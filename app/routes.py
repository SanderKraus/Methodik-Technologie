from app.utils import (
    clean_dataframe,
    preprocess_item_df,
    merge_data,
)
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

        df_ref = clean_dataframe(df_ref)
        df_ecr = clean_dataframe(df_ecr)

        df_chainged = merge_data(df_ref, df_ecr)
        df_new = merge_data(df_ecr, df_ref)

        return redirect(url_for("routes.index", df_chainged=df_chainged, df_new=df_new))
    return render_template("upload.html", form=form)
