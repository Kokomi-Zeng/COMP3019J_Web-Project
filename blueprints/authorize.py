from flask import Blueprint, render_template, request,redirect,jsonify
from .forms import LoginForm
from flask import session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db
#. 表示当前目录
from .forms import RegisterForm
from models import User

# 创建蓝图对象,第一个：蓝图名字，第二个；__name__表示代表当前的模块，第三个：url_prefix表示前缀，所有的在这里面的路由都会加上这里的前缀
bp = Blueprint("authorize", __name__, url_prefix="/authorize")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    form = LoginForm(request.form)
    if form.validate():
        phone = form.phone.data
        password = form.password.data

        user = User.query.filter_by(phone=phone).first()
        if user and check_password_hash(user.password, password):
            # 密码验证通过
            session['user_phone'] = user.phone
            session['user_type'] = user.user_type
            return jsonify(success=True, message="Login successful")
        else:
            # 登录失败
            return jsonify(success=False, message="Incorrect phone or password.")
    else:
        return jsonify(success=False, errors=form.errors)

@bp.route("/register" , methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    # （先进行表单验证，用flask-wtf）
    form = RegisterForm(request.form)
    # 该方法会自动调用验证器以及内部validate方法
    if form.validate():
        phone = form.phone.data
        password = form.password.data
        user_type = form.user_type.data
        # 保存到数据库
        user = User(phone=phone, password=generate_password_hash([password]), user_type=user_type)
        # 用于数据库交互(不是管理用户会话)
        db.session.add(user)
        db.session.commit()
        return jsonify(success=True, message="Registration successful")
        # return redirect("/authorize/login")
    else:
        print(form.errors)
        return jsonify(success=False, errors=form.errors)
        # redirect("/authorize/register")

