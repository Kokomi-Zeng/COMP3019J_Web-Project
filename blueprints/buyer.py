from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.security import check_password_hash

from exts import db
from models import Product, Comment, Buyer, User, Purchase

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

@buyer_bp.route('/charge', methods=['GET'])
def charge():
    phone = request.args.get('phone')
    try:
        charge_num = float(request.args.get('charge_num'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid charge amount."}), 400
    password = request.args.get('password')

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

@buyer_bp.route('/buyerItem', methods=['GET'])
def get_buyer_items():
    phone = request.args.get('phone')
    buyer = Buyer.query.filter_by(phone=phone).first()

    if not buyer:
        return jsonify({"error": "Buyer not found"}), 404

    purchased_items = []
    for purchase in buyer.purchases:
        purchased_items.append({
            'product_name': purchase.product.product_name,
            'total_price': purchase.purchase_price * purchase.purchase_number,
            'image_src': purchase.image_src_at_time_of_purchase,
            'purchase_time': purchase.purchase_time.strftime('%Y-%m-%d %H:%M:%S'),
            'purchase_quantity': purchase.purchase_number
        })

    return jsonify(purchased_items), 200


@buyer_bp.route('/buyItem', methods=['GET'])
def buy_item():
    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid product ID."}), 400

    phone = request.args.get('phone')

    buyer = Buyer.query.filter_by(phone=phone).first()
    product = Product.query.filter_by(product_id=product_id).first()

    # 判断买家和商品是否存在
    if not buyer or not product:
        return jsonify({"error": "Buyer or product not found"}), 404

    # 判断买家账户的钱是否足够
    if buyer.balance < product.price:
        return jsonify({"success": False, "error": "Insufficient funds"}), 400

    # balance减少，storage减少，新的purchase添加到数据库中
    buyer.balance -= product.price
    product.storage -= 1

    new_purchase = Purchase(
        product_id=product.product_id,
        buyer_phone=buyer.phone,
        purchase_number=1,
        purchase_price=product.price,
        purchase_time=datetime.now(),
        image_src_at_time_of_purchase=product.image_src
    )

    db.session.add(new_purchase)
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

