import numpy as np
import pandas as pd

THRESHOLD_NUNIQUE_SIZE = 2


def infer_types(df_original: pd.DataFrame) -> pd.DataFrame:
    df = df_original.copy()

    # Make sure that all columns names are strings
    df.columns = df.columns.astype(str)

    # Replace +-inf with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    for i in df.select_dtypes(include=["object"]).columns:
        # try to convert into integer
        try:
            df[i] = df[i].astype("int64")
            continue
        except ValueError:
            pass

        # try to convert into datetime
        try:
            df[i] = pd.to_datetime(df[i], errors="ignore", infer_datetime_format=True)
            continue
        except ValueError:
            pass

    # Convert bool or pandas category columns to categorical (object)
    for i in df.select_dtypes(include=["bool", "category"]).columns:
        df[i] = df[i].astype("object")

    # Pandas interprets an integer columns containing missing values as a float column.
    for i in df.select_dtypes(include=["float64"]).columns:
        count_rows = len(df[i])
        count_unique = df[i].nunique()
        count_nan = sum(df[i].isnull())
        count_int = sum([v.is_integer() for v in df[i]])
        count_others = len(df[i]) - count_int - count_nan

        # if the column has integer values and NaNs, then it is an integer column

    return df
