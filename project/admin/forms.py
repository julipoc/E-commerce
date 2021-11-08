from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from flask_admin.form import ImageUploadField
from project import basename
from werkzeug.utils import secure_filename
import os.path as op


def thumb_name(filename):
    name, _ = op.splitext(filename)
    return secure_filename("%s-thumb.jpg" % name)


class AddProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = IntegerField("Price (€)", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired(), Length(max=65)])
    category = SelectField("Category", validators=[DataRequired()], choices=["bracelet", "earring", "necklace", "ring"])
    subcategory = SelectField("Subcategory", validators=[DataRequired()], choices=["gold", "silver"])
    stock = IntegerField("In stock", validators=[DataRequired()])
    image = ImageUploadField("Image", thumbgen=thumb_name, base_path=basename, validators=[DataRequired()])


class AddUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])


class AddOrderForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    country = SelectField("Country", validators=[DataRequired()], choices=["Afghanistan", "Albania", "Algeria", "Andorra", "Angola","Antigua & Deps","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina","Burundi","Cambodia","Cameroon","Cape Verde","Central African Rep","Chad","Chile","China","Colombia","Comoros","Congo","Congo {Democratic Rep}","Costa Rica","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland {Republic}","Israel","Italy","Ivory Coast","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Korea North","Korea South","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar, {Burma}","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russian Federation","Rwanda","St Kitts & Nevis","St Lucia","Saint Vincent & the Grenadines","Samoa","San Marino","Sao Tome & Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad & Tobago","Tunisia","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam", "Yemen", "Zambia", "Zimbabwe"])
    city = StringField("City", validators=[DataRequired()])
    zip_code = IntegerField("Zip code", validators=[DataRequired(), NumberRange(min=10000, max=99999,
                                                                                message="Enter a 5-digit zip code")])
    address = StringField("Address", validators=[DataRequired()])
    card_number = IntegerField("Card number",
                               validators=[DataRequired(),
                                           NumberRange(min=1000000000000000, max=9999999999999999,
                                                       message="Enter a 16-digit card number with no space")])
    security_number = IntegerField("CVV", validators=[DataRequired(),
                                                      NumberRange(min=100, max=999,
                                                                            message="Enter a 3-digit security code")])
    card_date = StringField("Expiration date", validators=[DataRequired(),
                                                           Length(min=5, max=5,
                                                                  message="Date must be in format mm/yy (e.g. 01/21)")],
                            render_kw={"placeholder": "mm/yy"})
