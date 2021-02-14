from app.database import compare_all_classifiers, insert_df
from app.forms import UploadForm
import pandas as pd
from flask import Blueprint, request, render_template, redirect, url_for


routes = Blueprint('routes', __name__, url_prefix='/')


@routes.route('/')
def index():
    compare_all_classifiers()
    return "Hallo Welt"


@routes.route('/techs')
def techs():
    return "Neue Techs"


@routes.route('/item')
def item():
    return "Neues Referenzbauteil"


@routes.route('/tech_kette')
def tech_chain():
    return "tech_Kette"


@routes.route('/compare')
def compare_item():
    return 'vergleich'


@routes.route("/upload", methods=["GET", "POST"])
def test():
    form = UploadForm()
    if form.validate_on_submit():
        insert_df(pd.read_excel(form.techs.data), 'techs')
        insert_df(pd.read_excel(form.item_com.data, header=1), 'item_com')
        insert_df(pd.read_excel(form.item_ref.data, header=1), 'item_ref')
        return redirect(url_for('routes.index'))
    return render_template("upload.html", form=form)
