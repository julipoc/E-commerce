from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from project.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField("", validators=[DataRequired()])
    last_name = StringField("", validators=[DataRequired()])
    email = StringField("", validators=[DataRequired(), Email()])
    password = PasswordField("", validators=[DataRequired(), EqualTo("confirm_password",
                                                                     message="Passwords must match!"),
                                             Length(min=5, max=10)])
    confirm_password = PasswordField("", validators=[DataRequired()])
    submit = SubmitField("CREATE AN ACCOUNT")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Your email has been registered already!")


class LoginForm(FlaskForm):
    email = StringField("", validators=[DataRequired(), Email()])
    password = PasswordField("", validators=[DataRequired()])
    submit = SubmitField("LOG IN")

    def validate_email(self, email):
        if "@" in email.data and not User.query.filter_by(email=email.data).first():
            raise ValidationError("Incorrect email address!")

    def validate_password(self, password):
        form = LoginForm()
        user = User.query.filter_by(email=form.email.data).first()
        if user and not user.check_password(password.data):
            raise ValidationError("Incorrect password!")
