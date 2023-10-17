from flask import Blueprint, render_template, session, request, jsonify
from werkzeug.security import generate_password_hash

from exts import db

seller_bp = Blueprint('seller', __name__, url_prefix='/seller')

from models import Product, Comment, Buyer, User, Seller

@seller_bp.route('/')
def seller():
    user_info = get_user_info()

    # **user_info相当于phone=user_info['phone'], name=user_info['name'], type=user_info['type']
    return render_template('seller.html', **user_info)


@seller_bp.route('/sellerInfo', methods=['GET'])
def seller_info():
    phone = request.args.get('phone')

    # 假如没有传入phone，返回服务器200状态码，表示请求成功，但是没有数据
    if not phone:
        # return jsonify({"data": None}), 200
        return jsonify([])

    seller = Seller.query.filter_by(phone=phone).first()
    # 假如用户不存在，返回服务器200状态码，表示请求成功，但是没有数据
    if not seller:
        # return jsonify({"data": None}), 200
        return jsonify([])

    return jsonify({
        "phone": seller.phone,
        # 事实上，这里不能返回密码，因为密码是加密的，除非不让加密，但这不合理，建议直接不显示得了
        # "password": seller.user.password,
        "name": seller.name,
        "introduction": seller.description,
    })

@seller_bp.route('/modifySellerInfo', methods=['POST'])
def modify_seller_info():
    phone = request.json.get('phone')
    name = request.json.get('name')
    introduction = request.json.get('introduction')
    password = request.json.get('password')

    # 验证 phone 是否存在
    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    seller = Seller.query.filter_by(phone=phone).first()
    # 判断卖家是否存在
    if not seller:
        return jsonify({"error": "Seller not found"}), 404

    # 更新卖家信息
    if name:
        seller.name = name
    if introduction:
        seller.description = introduction

    if password:
        # 加密
        hashed_password = generate_password_hash(password)
        seller.user.password = hashed_password

    db.session.commit()

    return jsonify({"message": "Seller information updated successfully"}), 200


def get_user_info():
    phone = session.get('phone')

    # 先判断session中是否有phone，如果没有，返回None
    if not phone:
        return {
            # 'phone': None,
            # 'name': None,
            'phone': "",
            'name': "",
        }

    # 如果有phone，但是数据库中没有该用户，返回None
    user = User.query.get(phone)
    if not user:
        return {
            # 'phone': None,
            # 'name': None,
            'phone': "",
            'name': "",
        }

    # 根据用户类型获取姓名, 里面的if判断是为了防止数据库中没有该用户的信息，导致程序报错
    if user.user_type == '0':  # 卖家
        if user.seller:
            name = user.seller.name
        else:
            # name = None
            name = ""
    elif user.user_type == '1':  # 买家
        if user.buyer:
            # name = user.buyer.name
            name = ""
        else:
            # name = None
            name = ""
    else:
        # name = None
        name = ""

    # 判断name是否为空字符串(是个游客或者卖家)
    if name == "":
        return {
            'phone': "",
            'name': "",
        }
    else:
        return {
            'phone': phone,
            'name': name,
        }
