from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class FilterForm(FlaskForm):
    subcategory_filter = RadioField("", choices=["all products", "gold", "silver"], default="all products",
                                    validators=[DataRequired()])
    submit = SubmitField("APPLY")
