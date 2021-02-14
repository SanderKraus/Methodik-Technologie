from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    techs = FileField('Technologien', validators=[
        FileRequired(),
        FileAllowed(['xlsx'])
    ])
    item_ref = FileField('Referenz Bauteil', validators=[
        FileRequired(),
        FileAllowed(['xlsx'])
    ])
    item_com = FileField('Vergleichs Bauteil', validators=[
        FileRequired(),
        FileAllowed(['xlsx'])
    ])
