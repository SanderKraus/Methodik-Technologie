from typing import List
import pandas as pd


def preprocess_item_df(df: pd.DataFrame) -> dict:
    df.columns = clean_column_names(df.columns.tolist())
    json_df = [
        row.dropna().to_dict() for index, row in df.apply(clean_values).iterrows()
    ]
    return {"data": json_df}


def clean_values(x: pd.Series) -> pd.Series:
    if x.dtypes == "object":
        try:
            x = pd.Series(
                [
                    i.replace("mm", "").replace(",", ".").strip()
                    for i in x.dropna().apply(str)
                ]
            ).astype("float64")
        except ValueError:
            x = x.dropna().astype("string")
    return x


def clean_column_names(col_names: List[str]) -> List:
    return [name.split(":")[0].strip() for name in col_names]


def clean_datatech(df: pd.DataFrame) -> pd.DataFrame:

    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.iloc[:, :-1]
    df.columns = clean_column_names(df.columns.tolist())
    for name, col in df.iteritems():
        x = col.apply(str).str.replace("mm", "")
        y = x.str.replace(",", ".")
        try:
            y = y.astype("float64")
        except ValueError:
            y = y.astype("string")
        df[name] = y
    return df


def merge_data(df: pd.DataFrame, df_1: pd.DataFrame) -> pd.DataFrame:
    df = df.merge(df_1, how="outer", indicator=True).loc[
        lambda x: x["_merge"] == "left_only"
    ]
    df = df.reset_index(drop=True)
    return df


def clean_merkmale(df):
    df = df[df.columns.drop(list(df.filter(like="+")))]
    df = df[df.columns.drop(list(df.filter(like="-")))]
    return df
