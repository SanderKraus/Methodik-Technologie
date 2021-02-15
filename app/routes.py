from app.utils import clean_column_names, clean_values_sql, preprocess_item_df
from app.forms import UploadForm, UploadTechForm, UploadItemComForm, UploadItemRefForm
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

        df_ref = df_ref.iloc[:, :-1]
        df_ecr = df_ecr.iloc[:, :-1]

        df_ref.columns = clean_column_names(df_ref.columns.tolist())
        df_ecr.columns = clean_column_names(df_ecr.columns.tolist())

        for name, col in df_ref.iteritems():
            x = col.apply(str).str.replace("mm", "")
            y = x.str.replace(",", ".")
            try:
                y = y.astype("float64")
            except ValueError:
                y = y.astype("string")
            df_ref[name] = y
        print(df_ref)

        # df_deleted = df_ref.merge(df_ecr, how="outer", indicator=True).loc[
        #     lambda x: x["_merge"] == "left_only"
        # ]
        # df_deleted = df_deleted.reset_index(drop=True)
        # index_deleted = df_deleted.index

        # number_of_rows_deleted = len(index_deleted)

        # df_new = df_ref.merge(df_ecr, how="outer", indicator=True).loc[
        #     lambda x: x["_merge"] == "right_only"
        # ]
        # df_new = df_new.reset_index(drop=True)
        # index_new = df_new.index

        # number_of_rows_new = len(index_new)

        # df = pd.concat([df_ref, df_ecr])
        # df = df.drop_duplicates(keep=False)
        # print(df)
        # df = df.reset_index(drop=True)

        # df_gpby = df.groupby(list(df.columns))

        # idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]

        return redirect(url_for("routes.index"))
    return render_template("upload.html", form=form)
