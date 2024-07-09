import json
from io import StringIO
from typing import BinaryIO

import pandas as pd

from .data_matching import find_data_matching_among_df, find_schema_matching_among_df


def find_schema_matching(target_name: str, target_file: BinaryIO, source_name: str, source_file: BinaryIO):
    target_df = pd.read_csv(target_file)
    source_df = pd.read_csv(source_file)

    matching = find_schema_matching_among_df(target_name, target_df, source_name, source_df)

    target_data_matched_columns = list(matching.keys())
    tmp = []
    for v in matching.values():
        tmp += v
    source_data_matched_columns = list(set(tmp))

    response = {
        "target_data_columns": target_df.columns.tolist(),
        "target_data_matched_columns": target_data_matched_columns,
        "source_data_columns": source_df.columns.tolist(),
        "source_data_matched_columns": source_data_matched_columns,
        "matching": matching
    }
    return response


def find_data_matching(target_file: BinaryIO, source_file: BinaryIO, matching: str) -> StringIO:
    matching_dict = json.loads(matching)

    target_df = pd.read_csv(target_file)
    source_df = pd.read_csv(source_file)

    data_matching_result = find_data_matching_among_df(target_df, source_df, matching_dict)

    pair_columns = ["__target_index", "__source_index"]
    pair_df = pd.DataFrame(data_matching_result, columns=pair_columns)
    merged_df = target_df.merge(pair_df, left_index=True, right_on="__target_index", how="left")
    for col in source_df.columns:
        col_tmp = col
        if col_tmp in merged_df.columns:
            col_tmp = col_tmp + "_source"
        merged_df[col_tmp] = merged_df["__source_index"].map(source_df[col])

    merged_df = merged_df.drop(columns=pair_columns, axis=1)

    # DataFrameをCSV形式に変換
    buffer = StringIO()
    merged_df.to_csv(buffer, index=False)
    buffer.seek(0)

    return buffer
