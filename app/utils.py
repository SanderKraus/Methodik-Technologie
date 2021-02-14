import pandas as pd


def compare_features():

    df_1 = df_1.iloc[:, :-1]
    df_2 = df_2.iloc[:, :-1]

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

    # print(number_of_rows_deleted)
    # print(number_of_rows_new)
