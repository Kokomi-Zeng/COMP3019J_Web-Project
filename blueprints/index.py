from flask import Blueprint, render_template, session, jsonify
from models import User

bp = Blueprint('index', __name__, url_prefix='/')
# 这个是给base.html用的，我假设index.html是base.html的子模板


@bp.route('/')
def index():
    user_info = get_user_info()
    # **user_info相当于phone=user_info['phone'], name=user_info['name'], type=user_info['type']
    return render_template('index.html', **user_info)


@bp.route('/getSession')
def getSession():
    phone = session.get('phone')
    user = User.query.get(phone)
    if user:
        if user.user_type == '0':
            name = user.seller.name
        if user.user_type == '1':
            name = user.buyer.name
        return {'phone': phone, 'name': name}
    else:
        # return {'phone': None, 'name': None}
        return {'phone': "", 'name': ""}


def get_user_info():
    phone = session.get('phone')

    # 先判断session中是否有phone，如果没有，返回None
    if not phone:
        return {
            # 'phone': None,
            # 'name': None,
            # 'type': None
            'phone': "",
            'name': "",
            'type': ""
        }

    # 如果有phone，但是数据库中没有该用户，返回None
    user = User.query.get(phone)
    if not user:
        return {
            # 'phone': None,
            # 'name': None,
            # 'type': None
            'phone': "",
            'name': "",
            'type': ""
        }

    # 根据用户类型获取姓名, 里面的if判断是为了防止数据库中没有该用户的信息，导致程序报错
    if user.user_type == '0':  # 卖家
        if user.seller:
            name = user.seller.name
        else:
            name = ""
    elif user.user_type == '1':  # 买家
        if user.buyer:
            name = user.buyer.name
        else:
            name = ""
    else:
        name = ""

    # 判断name是否为空字符串(是个游客)
    if name == "":
        return {
            'phone': "",
            'name': "",
            'type': ""
        }
    else:
        return {
            'phone': phone,
            'name': name,
            'type': user.user_type
        }
