import pandas as pd
from logging import getLogger
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS

from core.llm_adapter.factory import LlmFactory
from core.vector_db_adapter.custom_embedding import CustomEmbedding

logger = getLogger("uvicorn.app")


PROMPT_COLUMN_DESCRIPTION_TEMPLATE = """Your task is to generate a description (30 words max) of a target column in a tabular data as one of business metadata.
Here is table name (file name) and some details about the columns in the table:
Table name: {TABLE_NAME}
Target column name: {COLUMN_NAME}

Description:
"""

PROMPT_SCHEMA_MATCHING_TEMPLATE = """Your task is to determine if the two attributes (columns) are semantically equivalent or relevant in the context of matching data between two tables.
Each attribute will be provided by its name and a brief description.
Your goal is to assess if they refer to the same information based on these names and descriptions provided.

---
Examples:
Attribute A is [name: Address, description: This column contains the address information].
Attribute B is [name: Street, description: User's home street].
Answer: Yes

Attribute A is [name: 住所, description: This column contains the address information].
Attribute B is [name: 市区町村名, description: This column represents the names of cities, wards, and towns in a specific region.].
Answer: Yes

Attribute A is [name: 住所, description: This column contains the address information].
Attribute B is [name: 都道府県名, description: This column represents the names of prefectures.].
Answer: Yes
---

Attribute A is [name: {ATTR_A_NAME}, description: {ATTR_A_DESC}].
Attribute B is [name: {ATTR_B_NAME}, description: {ATTR_B_DESC}].
Are Attribute A and Attribute B semantically equivalent or relevant? Choose your answer from: [Yes, No].
"""

PROMPT_ENTITY_MATCHING_TEMPLATE = """You are tasked with determining whether two records listed below are the same based on the information provided.
Carefully compare the {ATTRIBUTE_LIST} for each record before making your decision.  
Note: Missing values (N/A or \"nan\") should not be used as a basis for your decision.  

Record A: {RECORD_A}
Record B: {RECORD_B}
Are record A and record B the same entity? Choose your answer from: [Yes, No]"""


def extract_unique_columns(df: pd.DataFrame):
    result = []
    for c in df.columns:
        count_rows = len(df[c])
        count_unique = df[c].nunique()
        ratio_unique = count_unique / count_rows

        if count_unique > 2 and ratio_unique >= 0.1:
            result.append(c)
    return result


def process_df(name: str, df: pd.DataFrame):
    logger.debug("Starting to process dataframe: %s", name)
    unique_columns = extract_unique_columns(df)
    column_description = []
    for c in unique_columns:
        logger.debug("Processing column: %s", c)
        factory = LlmFactory()
        llm = factory.get_llm()
        r = llm.completion(
            PROMPT_COLUMN_DESCRIPTION_TEMPLATE.format(TABLE_NAME=name, COLUMN_NAME=c)
        )
        column_description.append(r)
    return unique_columns, column_description


def find_schema_matching_among_df(
    target_name: str,
    target_df: pd.DataFrame,
    source_name: str,
    source_df: pd.DataFrame,
):
    logger.debug(
        "Starting to find schema matching between %s and %s", target_name, source_name
    )
    unique_columns_target, column_description_target = process_df(
        target_name, target_df
    )
    unique_columns_source, column_description_source = process_df(
        source_name, source_df
    )

    # find column matching
    matching = {}
    for i, c_t in enumerate(unique_columns_target):
        # NOTE: This is a naive implementation. In the future, we should consider using a kNN search to find the better matching efficiently.
        for j, c_s in enumerate(unique_columns_source):
            logger.debug("Processing target column: %s, source column: %s", c_t, c_s)
            factory = LlmFactory()
            llm = factory.get_llm()
            r = llm.completion(
                PROMPT_SCHEMA_MATCHING_TEMPLATE.format(
                    ATTR_A_NAME=c_t,
                    ATTR_A_DESC=column_description_target[i],
                    ATTR_B_NAME=c_s,
                    ATTR_B_DESC=column_description_source[j],
                )
            )

            if r.startswith("Yes"):
                logger.debug("Matched target column: %s, source column: %s", c_t, c_s)
                matching.setdefault(c_t, []).append(c_s)

    return matching


def entity_matching(record_a, record_b):
    attribute_list = ", ".join(list(record_a.keys()) + list(record_b.keys()))
    record_a_str = ', '.join([f"{col}: {val}" for col, val in record_a.items()])
    record_b_str = ', '.join([f"{col}: {val}" for col, val in record_b.items()])
    prompt = PROMPT_ENTITY_MATCHING_TEMPLATE.format(
        ATTRIBUTE_LIST=attribute_list,
        RECORD_A=record_a_str,
        RECORD_B=record_b_str
    )
    factory = LlmFactory()
    llm = factory.get_llm()
    r = llm.completion(prompt)
    if r.startswith("Yes"):
        return True
    return False


def find_data_matching_among_df(target_df: pd.DataFrame, source_df: pd.DataFrame, matching: dict):
    # create FAISS index
    db = {}
    for tk in matching:
        for source_key in matching[tk]:
            if source_key in db:
                continue
            logger.debug("Creating FAISS index for source column: %s", source_key)
            raw_documents = []
            for source_index, source_row in source_df.iterrows():
                raw_documents.append(
                    Document(page_content=source_row[source_key], metadata={"index": source_index})
                )
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            documents = text_splitter.split_documents(raw_documents)
            # NOTE: Use naive FAISS class instead of FaissDB class for on-memory indexing
            db[source_key] = FAISS.from_documents(documents, CustomEmbedding())
    
    # matching
    matched_source_index_set = set()
    matched_list = []
    for target_index, target_row in target_df.iterrows():
        logger.debug("Processing target row: %s", target_index)
        retrieved_source_index_set = set()
        for target_key in matching:
            query = str(target_row[target_key])
            for source_key in matching[target_key]:
                similar_records = db[source_key].similarity_search_with_score(query, k=10)
                for r, score in similar_records:
                    if score > 0.15:
                        break
                    retrieved_source_index_set.add(r.metadata["index"])
        
        target_keys = list(matching.keys())
        target_record = target_row[target_keys]
        source_keys = list(db.keys())

        for source_index in retrieved_source_index_set:
            if source_index in matched_source_index_set:
                # NOTE: This is to prevent duplicate matching (under unique assumtion)
                continue
            source_row = source_df.iloc[source_index]
            source_record = source_row[source_keys]

            is_matched = entity_matching(target_record, source_record)
            if is_matched:
                logger.debug("Matched target row: %s, source row: %s", target_index, source_index)
                matched_source_index_set.add(source_index)
                matched_list.append((target_index, source_index))
                break
    
    return matched_list
            
            