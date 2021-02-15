from app.utils import preprocess_item_df
from app.forms import UploadForm, UploadTechForm, UploadItemForm
from app.database import mongo_insert, mongo_delete_collection, mongo_get_one, compare_item_collections
import pandas as pd
from flask import Blueprint, request, render_template, redirect, url_for, g

routes = Blueprint('routes', __name__, url_prefix='/')


@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/techs')
def techs():
    return "techs"


@routes.route('/item/<name>', methods=['GET', 'POST'])
def item(name):
    form = UploadItemForm()
    if form.validate_on_submit():
        item_dict = preprocess_item_df(pd.read_excel(
            form.item.data, header=1))
        mongo_delete_collection(name)
        mongo_insert(f"{name}_features", item_dict)
    return render_template("item.html", form=form, name=name)


@routes.route('/tech_kette')
def tech_chain():
    return "tech_Kette"


@routes.route('/compare')
def compare():
    results = compare_item_collections()
    return render_template('compare.html', results=results)


@ routes.route("/upload", methods=["GET", "POST"])
def test():
    form = UploadForm()
    if form.validate_on_submit():
        df_ref = pd.read_excel(form.item_ref.data, header=1)
        df_ecr = pd.read_excel(form.item_com.data, header=1)

        df_ref = df_ref.iloc[:, :-1]
        df_ecr = df_ecr.iloc[:, :-1]

        print(df_ref)
        print(df_ecr)

        df_deleted = df_ref.merge(df_ecr, how="outer", indicator=True).loc[
            lambda x: x["_merge"] == "left_only"
        ]
        df_deleted = df_deleted.reset_index(drop=True)
        index_deleted = df_deleted.index
        print(df_deleted)
        number_of_rows_deleted = len(index_deleted)

        print(number_of_rows_deleted)

        df_new = df_ref.merge(df_ecr, how="outer", indicator=True).loc[
            lambda x: x["_merge"] == "right_only"
        ]
        df_new = df_new.reset_index(drop=True)
        index_new = df_new.index
        print(df_new)
        number_of_rows_new = len(index_new)

        # df = pd.concat([df_ref, df_ecr])
        # df = df.drop_duplicates(keep=False)
        # print(df)
        # df = df.reset_index(drop=True)

        # df_gpby = df.groupby(list(df.columns))

        # idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]

        return redirect(url_for('routes.index'))
    return render_template("upload.html", form=form)
