import sqlite3
from typing import List
import pandas as pd
from pandas.core.frame import DataFrame


def insert_df(df: DataFrame, name: str):
    try:
        with sqlite3.connect("database.db") as con:
            df.to_sql(name, con=con)
    except:
        con.rollback()


def get_df(name: str):
    try:
        with sqlite3.connect("database.db") as con:
            df = pd.read_sql(f"SELECT * FROM {name}", con=con)
            return df
    except:
        con.rollback()


"""
df_deleted = df_1.merge(df_2, how="outer", indicator=True).loc[
                lambda x: x["_merge"] == "left_only"
            ]
            df_deleted = df_deleted.reset_index(drop=True)
            index_deleted = df_deleted.index
            number_of_rows_deleted = len(index_deleted)

            df_new = df_1.merge(df_2, how="outer", indicator=True).loc[
                lambda x: x["_merge"] == "right_only"
            ]
            df_new = df_new.reset_index(drop=True)
            index_new = df_new.index
            number_of_rows_new = len(index_new)
"""


def compare_all_classifiers():
    cl_com = get_df('item_com')['Classifier'].drop_duplicates()
    cl_ref = get_df('item_ref')['Classifier'].drop_duplicates()

    res = []
    for cl in cl_com:
        if cl in cl_ref:
            res.append(cl)

    if len(res) > 0:
        for cl in res:
            if cl in get_df('techs')['technologie'].drop_duplicates():
                print('Es gibt eine Tech die das kann')
    else:
        compare_fuzz_attributes(res)


def compare_fuzz_attributes(res: List):
    for feature in res:

        #possible_class = get_df('techs')['technologie'].drop_duplicates()
        # Vergleiche attr_com mit possible Attr
        # Ergebnis: Sind Merkmale durchfuerbar

        # 1. Keine Neue Classifier
        # Wenn neue Classifier
        #   2. Wenn Classifier nicht in Techs dann "Neue Technologie vom Techplaner anlegen"
        #   3. Wenn Classifier in Techs dann "Vergleiche Tech mit Feature"
