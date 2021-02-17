from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadTechForm(FlaskForm):
    """
    TODO@ MUSS NOCH ANGEPASST WERDEN
    NICHT BENUTZEN
    """

    name = FileField("hello", validators=[FileRequired(), FileAllowed(["xlsx"])])


class UploadItemRefForm(FlaskForm):
    item_ref = FileField(
        "Referenz Bauteil",
        render_kw={"class": "form-control"},
        validators=[FileRequired(), FileAllowed(["xlsx"])],
    )


class UploadItemComForm(FlaskForm):
    item_ref = FileField(
        "Vergleichs Bauteil", validators=[FileRequired(), FileAllowed(["xlsx"])]
    )


class UploadForm(FlaskForm):
    item_ref = FileField(
        "Referenz Bauteil", validators=[FileRequired(), FileAllowed(["xlsx"])]
    )
    item_com = FileField(
        "Vergleichs Bauteil", validators=[FileRequired(), FileAllowed(["xlsx"])]
    )
    item_tech = FileField(
        "Referenz Technologie", validators=[FileRequired(), FileAllowed(["xlsx"])]
    )
