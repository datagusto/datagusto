from services.llm.load import llm

prompt = """
You are an AI assistant that helps people to generate
description for table columns.

Here is table name and some details about the columns in the table:
Table name: {TABLE_NAME}
Column details: {COLUMN_DETAILS}

Please generate one sentence description for the column.
"""


def generate_column_description(column_info: dict, table_name) -> str:
    column_data = ""
    for key, value in column_info.items():
        column_data += f"{key}: {value}\n"

    _full_prompt = prompt.format(
        TABLE_NAME=table_name,
        COLUMN_DETAILS=column_data
    )

    res = llm.completion(_full_prompt)
    return res

