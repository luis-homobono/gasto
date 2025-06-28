from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField, ValidationError


class LoginForm(FlaskForm):
    email = StringField(
        "Correo electronico",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "example@example.com"},
    )
    password = PasswordField(
        "Contraseña", validators=[DataRequired()], render_kw={"placeholder": "********"}
    )
    submit = SubmitField("Iniciar sesión")
