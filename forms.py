import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import (
        DataRequired,
        Length,
        EqualTo,
        ValidationError
)

def password_check(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None

    password_ok = not (
        length_error
        or digit_error
        or uppercase_error
        or lowercase_error
    )

    return {
        "password_ok": password_ok,
        "length_error": length_error,
        "digit_error": digit_error,
        "uppercase_error": uppercase_error,
        "lowercase_error": lowercase_error,
    }

class LoginForm(FlaskForm):
        username = StringField("Username", validators=[DataRequired(), Length(min=4, max=24)])
        password = PasswordField("Password", validators=[DataRequired()])
        
class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=24)]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    confirm = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password")]
    )

    def validate_password(self, field):
        result = password_check(field.data)

        if not result["password_ok"]:
            if result["length_error"]:
                raise ValidationError("Password must be at least 8 characters long")
            if result["digit_error"]:
                raise ValidationError("Password must contain a digit")
            if result["uppercase_error"]:
                raise ValidationError("Password must contain an uppercase letter")
            if result["lowercase_error"]:
                raise ValidationError("Password must contain a lowercase letter")

class NoteForm(FlaskForm):
        title = StringField("Title", validators=[
                Length(max=100)
        ])
        content = TextAreaField("Content", validators=[
                DataRequired()
        ])
        submit = SubmitField("Save")