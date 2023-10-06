from flask import Blueprint, render_template, request, jsonify, session

from models import Product, Comment, Buyer, User

base_bp = Blueprint('base', __name__, url_prefix='/base')


@base_bp.route('/')
def base():
    user_info = get_user_info()

    # **user_info相当于phone=user_info['phone'], name=user_info['name'], type=user_info['type']
    return render_template('shop.html', **user_info)


def get_user_info():
    phone = session.get('phone')

    # 先判断session中是否有phone，如果没有，返回None
    if not phone:
        return {
            'phone': None,
            'name': None,
            'type': None
        }

    # 如果有phone，但是数据库中没有该用户，返回None
    user = User.query.get(phone)
    if not user:
        return {
            'phone': None,
            'name': None,
            'type': None
        }

    # 根据用户类型获取姓名, 里面的if判断是为了防止数据库中没有该用户的信息，导致程序报错
    if user.user_type == '0':  # 卖家
        if user.seller:
            name = user.seller.name
        else:
            name = None
    elif user.user_type == '1':  # 买家
        if user.seller:
            name = user.buyer.name
        else:
            name = None
    else:
        name = None

    return {
        'phone': phone,
        'name': name,
        'type': user.user_type
    }