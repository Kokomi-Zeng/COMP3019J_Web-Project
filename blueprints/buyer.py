from flask import Blueprint, render_template, request, jsonify

from models import Product, Comment, Buyer

buyer_bp = Blueprint('buyer', __name__, url_prefix='/buyer')

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



