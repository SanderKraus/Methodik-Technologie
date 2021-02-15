from typing import List
import pandas as pd


def preprocess_item_df(df: pd.DataFrame) -> dict:
    df.columns = clean_column_names(df.columns.tolist())
    unique_classifiers = df['Classifier'].unique().tolist()
    json_df = [row.dropna().to_dict()
               for index, row in df.apply(clean_values).iterrows()]
    return {"data": json_df, "classifier": unique_classifiers, "counter": len(json_df)}

# def preprocess_item_df_sql(df: pd.DataFrame) -> dict:
#     df.columns = clean_column_names(df.columns.tolist())
#     json_df = [row.dropna().to_dict()
#                for index, row in df.apply(clean_values).iterrows()]
#     return {"data": json_df}


def clean_values(x: pd.Series) -> pd.Series:
    if x.dtypes == 'object':
        try:
            x = pd.Series([i.replace('mm', '').replace(
                ',', '.').strip() for i in x.dropna().apply(str)]).astype('float64')
        except ValueError:
            x = x.dropna().astype('string')
    return x


def clean_column_names(col_names: List[str]) -> List:
    return [name.split(':')[0].strip().lower() for name in col_names]
