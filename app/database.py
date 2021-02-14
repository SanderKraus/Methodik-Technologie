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
    pass

    # funktion: vergleiche Referenz-Bauteil mit Vergleichs-Bauteil
    #       0. Parameter:
    #           - DF[Ref_Bauteil]
    #           - DF[Vergleich_Bauteil]
    #       1. Vergleiche Dataframes auf Aenderung und neue Features
    #       2. RETURN: Liste von Featuren die neu dazugekommen sind oder sich veraendert haben (andere Werte, neues Merkmal)
    #
    # funktion: vergleiche feature mit Technologie
    #       0. Parameter:
    #           - Liste von Featuren die neu dazugekommen sind oder sich veraendert haben (andere Werte, neues Merkmal)
    #           - Alle Tech ||die eine Position haben||
    #       1. Sortiere Techologien nach Position
    #       2. Schleife: Fuer jede Tech in Technologien
    #           2.1 Vergleiche in der Schleife alle veraenderten und neuen Features mit dem Classifier von der Tech

    technologien = [1, 2, 3, 4]

    features = [7, 8, 9, 1]

    for feature in features:
        for tech in technologien:
            if tech['classifier'] in feature['classifier']:
                value_to_match = feature[tech['column_name_of_value']]
                tech[]
