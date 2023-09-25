import wtforms
from wtforms import validators
from models import User

class RegisterForm(wtforms.Form):
    phone = wtforms.StringField(validators=[validators.Length(min=8, max=20, message="phone number should be 8-20 digits")])
    password = wtforms.PasswordField(validators=[validators.Length(min=8, max=20, message="password should be 8-20 digits")])
    user_type = wtforms.SelectField(choices=[("buyer", "buyer"), ("seller", "seller")])

    # phone是否已经被注册（field代表的就是phone）
    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).first()
        if user:
            raise validators.ValidationError("phone number already registered")

class LoginForm(wtforms.Form):
    phone = wtforms.StringField(validators=[validators.Length(min=8, max=20, message="phone number should be 8-20 digits")])
    password = wtforms.PasswordField(validators=[validators.Length(min=8, max=20, message="password should be 8-20 digits")])





