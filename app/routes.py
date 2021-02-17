from app.utils import (
    clean_dataframe,
    preprocess_item_df,
    merge_data,
    clean_merkmale,
)
from app.forms import (
    UploadForm,
    UploadTechForm,
    UploadItemComForm,
    UploadItemRefForm,
)
from app.database import mongo_insert, mongo_delete_collection, mongo_get_one
import pandas as pd
from flask import Blueprint, request, render_template, redirect, url_for, g

routes = Blueprint("routes", __name__, url_prefix="/")


@routes.route("/")
def index():
    return render_template("index.html")


@routes.route("/techs")
def techs():
    return "techs"


@routes.route("/item", methods=["GET", "POST"])
def item():
    form = UploadItemRefForm()
    if form.validate_on_submit():
        ref_dict = preprocess_item_df(pd.read_excel(form.item_ref.data, header=1))
        mongo_delete_collection("ref_features")
        mongo_insert("ref_features", ref_dict)
    return render_template("ref_item.html", form=form)


@routes.route("/tech_kette")
def tech_chain():
    return "tech_Kette"


@routes.route("/compare")
def compare_item():
    return "vergleich"


@routes.route("/upload", methods=["GET", "POST"])
def test():
    form = UploadForm()
    if form.validate_on_submit():
        df_ref = pd.read_excel(form.item_ref.data, header=1)
        df_ecr = pd.read_excel(form.item_com.data, header=1)
        df_tech = pd.read_excel(form.item_tech.data)

        print(df_tech)
        df_ref = clean_dataframe(df_ref)
        df_ecr = clean_dataframe(df_ecr)

        df_chainged = merge_data(df_ref, df_ecr)
        df_new = merge_data(df_ecr, df_ref)

        df_chainged = clean_merkmale(df_chainged)
        df_new = clean_merkmale(df_new)

        # print(df_chainged)
        # print(df_new)

        return redirect(url_for("routes.index"))
    return render_template("upload.html", form=form)


@routes.route("/create_technology", methods=["GET", "POST"])
def create_technology():

    if request.method == "POST":
        conn = sqlite3.connect("app.db")
        cur = conn.cursor()
        name = request.form["name"]
        fähigkeit = request.form["fähigkeit0"]
        a = request.form["a0"]
        b = request.form["b0"]
        c = request.form["c0"]
        d = request.form["d0"]
        daten = {
            "Technologie": [name],
            fähigkeit + "_a": [a],
            fähigkeit + "_b": [b],
            fähigkeit + "_c": [c],
            fähigkeit + "_d": [d],
        }

        dataframe = pd.DataFrame(data=daten)

        try:
            # set techname = name
            data = pd.read_sql_query(
                "SELECT * FROM Technologien WHERE Technologie='" + name + "'", conn
            )
            data = data.loc[:, data.columns != "index"]

            if data.empty:
                # dataframe1 = dataframe
                dataframe_all = pd.read_sql_query("SELECT * FROM Technologien", conn)
                dataframe_all = dataframe_all.loc[:, dataframe_all.columns != "index"]
                dataframe1 = pd.concat([dataframe_all, dataframe])
            else:
                if not fähigkeit + "_a" in data.columns:
                    dataframe = dataframe.loc[:, dataframe.columns != "Technologie"]
                    dataframe_row = pd.concat([data, dataframe], axis=1)
                    dataframe_all = pd.read_sql_query(
                        "SELECT * FROM Technologien WHERE Technologie!='" + name + "'",
                        conn,
                    )
                    dataframe_all = dataframe_all.loc[
                        :, dataframe_all.columns != "index"
                    ]
                    dataframe1 = pd.concat([dataframe_all, dataframe_row])
                    print(dataframe_all)
                else:
                    data.at[0, fähigkeit + "_a"] = a
                    data.at[0, fähigkeit + "_b"] = b
                    data.at[0, fähigkeit + "_c"] = c
                    data.at[0, fähigkeit + "_d"] = d
                    dataframe_all = pd.read_sql_query(
                        "SELECT * FROM Technologien WHERE Technologie!='" + name + "'",
                        conn,
                    )
                    dataframe_all = dataframe_all.loc[
                        :, dataframe_all.columns != "index"
                    ]
                    dataframe1 = pd.concat([dataframe_all, data])

            # dataframe_all = pd.read_sql_query("SELECT * FROM Technologien", conn)
            # dataframe_final = pd.concat([dataframe_all, dataframe1])
        except:
            dataframe1 = dataframe
            print("Erster Eintrag")

        cur.execute("DROP TABLE IF EXISTS Technologien;")

        print(dataframe1)
        # print(dataframe_all)
        # print(dataframe_final)

        dataframe1.to_sql(
            "Technologien",
            conn,
            schema=None,
            if_exists="replace",
            index=True,
            index_label=None,
            chunksize=None,
            dtype=None,
            method=None,
        )

        conn.commit()
        technology_row = pd.read_sql_query(
            "SELECT * FROM Technologien WHERE Technologie='" + name + "'", conn
        )
        technology_matrix = pd.DataFrame()
        i = 2
        for j in range(
            0, (int((len(technology_row.columns) - 2) / 4))
        ):  ##loc benutzen um von spalte x bis y zu iterieren
            j = i + 4
            technology_4_row = technology_row.iloc[
                :, i:j
            ]  # column names müssen gelöscht werden damit man die einzelnen spalten untereinander führen kann
            technology_4_row.rename(
                columns={
                    technology_4_row.columns[0]: "a",
                    technology_4_row.columns[1]: "b",
                    technology_4_row.columns[2]: "c",
                    technology_4_row.columns[3]: "d",
                },
                inplace=True,
            )
            fähigkeit_name = technology_row.columns[i].replace("_a", "")
            technology_4_row.rename(index={0: fähigkeit_name}, inplace=True)
            technology_matrix = pd.concat([technology_matrix, technology_4_row])
            i = j

        technology_matrix = technology_matrix.dropna()
        Tabelle = technology_matrix.to_html(classes="table table-hover")
        print(technology_matrix)

        conn.close()

    try:
        return render_template(
            "main/create_technology.html", name=name, Tabelle=[Tabelle]
        )
    except:
        return render_template("main/create_technology.html")
