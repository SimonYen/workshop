from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            InputRequired(message="Username is required"),
            Length(
                min=4, max=25, message="Username must be between 4 and 25 characters"
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Password is required"),
            Length(
                min=6, max=35, message="Password must be between 6 and 35 characters"
            ),
        ],
    )
    submit = SubmitField("Login")
