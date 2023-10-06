from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.security import check_password_hash

from exts import db
from models import Product, Comment, Buyer, User

buyer_bp = Blueprint('buyer', __name__, url_prefix='/buyer')


@buyer_bp.route('/')
def buyer():
    user_info = get_user_info()

    # **user_info相当于phone=user_info['phone'], name=user_info['name']]
    return render_template('buyer.html', **user_info)

@buyer_bp.route('/buyerInfo', methods=['GET'])
def buyer_info():
    phone = request.args.get('phone')

    # 假如没有传入phone，返回服务器200状态码，表示请求成功，但是没有数据
    if not phone:
        return jsonify({"data": None}), 200

    buyer = Buyer.query.filter_by(phone=phone).first()
    # 假如用户不存在，返回服务器200状态码，表示请求成功，但是没有数据
    if not buyer:
        return jsonify({"data": None}), 200

    return jsonify({
        "phone": buyer.phone,

        # 事实上，这里不能返回密码，因为密码是加密的，除非不让加密，但这不合理，建议直接不显示得了
        # "password": buyer.user.password,

        "name": buyer.name,
        "introduction": buyer.description,
        "balance": buyer.balance
    })

@buyer_bp.route('/charge', methods=['POST'])
def charge():
    phone = request.form.get('phone')
    charge_num = float(request.form.get('charge_num'))
    password = request.form.get('password')

    # 查询用户
    user = User.query.filter_by(phone=phone).first()

    # 如果没有找到用户或密码不正确
    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False}), 400

    # 给用户充值
    buyer = Buyer.query.filter_by(phone=phone).first()
    if not buyer:
        return jsonify({"success": False}), 400
    buyer.balance += charge_num
    db.session.commit()

    return jsonify({"success": True}), 200


def get_user_info():
    phone = session.get('phone')

    # 先判断session中是否有phone，如果没有，返回None
    if not phone:
        return {
            'phone': None,
            'name': None,
        }

    # 如果有phone，但是数据库中没有该用户，返回None
    user = User.query.get(phone)
    if not user:
        return {
            'phone': None,
            'name': None,
        }

    # 根据用户类型获取姓名, 里面的if判断是为了防止数据库中没有该用户的信息，导致程序报错
    if user.user_type == '0':  # 卖家
        if user.seller:
            # name = user.seller.name
            # 因为是buyer的蓝图，所以这么设置none或者直接设置为user.buyer.name都可以(但是前者更好)
            name = None
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
    }

