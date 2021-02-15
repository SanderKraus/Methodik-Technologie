from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadTechForm(FlaskForm):
    """
    TODO@ MUSS NOCH ANGEPASST WERDEN
    NICHT BENUTZEN
    """
    name = FileField('hello', validators=[
        FileRequired(),
        FileAllowed(['xlsx'])
    ])


class UploadItemForm(FlaskForm):
    item = FileField('Bauteil', render_kw={"class": "form-control"}, validators=[
        FileRequired(),
        FileAllowed(['xlsx'])
    ])


class UploadForm(FlaskForm):
    item_ref = FileField('Referenz Bauteil', validators=[
        FileRequired(),
        FileAllowed(['xlsx'])
    ])
    item_com = FileField('Vergleichs Bauteil', validators=[
        FileRequired(),
        FileAllowed(['xlsx'])
    ])
