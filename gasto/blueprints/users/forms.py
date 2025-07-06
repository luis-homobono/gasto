from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField, ValidationError

from gasto.models import User


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


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    firstname = StringField("Nombres")
    lastname = StringField("Apellidos")
    email = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            EqualTo(
                "password_confirm", message="¡Las contraseñas deberían ser iguales!"
            ),
        ],
    )
    password_confirm = PasswordField(
        "Confirmar Contraseña", validators=[DataRequired()]
    )
    submit = SubmitField("¡Registrar!")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message="¡El correo ya ha sido registrado!")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(message="¡Tu username ya ha sido registrado!")
