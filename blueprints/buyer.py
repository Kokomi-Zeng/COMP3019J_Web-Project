from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import logging
from exts import db
from models import Product, Comment, Buyer, User, Purchase

buyer_bp = Blueprint('buyer', __name__, url_prefix='/buyer')
logging.basicConfig(level=logging.DEBUG)

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
        # return jsonify({"data": None}), 200
        phone = ""

    buyer = Buyer.query.filter_by(phone=phone).first()
    # 假如用户不存在，返回服务器200状态码，表示请求成功，但是没有数据
    if not buyer:
        # return jsonify({"data": None}), 200
        phone = ""

    if phone == "":
        return jsonify({
            "phone": "",
            "name": "",
            "introduction": "",
        })
    else:
        return jsonify({
            "phone": buyer.phone,

            # 事实上，这里不能返回密码，因为密码是加密的，除非不让加密，但这不合理，建议直接不显示得了
            # "password": buyer.user.password,

            "name": buyer.name,
            "introduction": buyer.description,
            # "balance": buyer.balance
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
        # return jsonify({"error": "Buyer not found"}), 404
        return jsonify([])

    purchased_items = []
    for purchase in buyer.purchases:
        purchased_items.append({
            'product_name': purchase.product.product_name,
            'total_price': purchase.purchase_price,
            'image_src': purchase.image_src_at_time_of_purchase,
            # 将datetime对象转换为字符串
            'purchase_time': purchase.purchase_time.strftime('%Y-%m-%d %H:%M:%S'),
            'purchase_quantity': purchase.purchase_number
        })

    return jsonify(purchased_items), 200


@buyer_bp.route('/buyItem', methods=['GET'])
def buy_item():
    # logging.debug("buyItem called.")
    try:
        product_id = int(request.args.get('product_id'))
        quantity = int(request.args.get('quantity', 1)) # 获取商品数量，如果未指定，默认为1
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid product ID or quantity."}), 400

    phone = request.args.get('phone')

    buyer = Buyer.query.filter_by(phone=phone).first()
    product = Product.query.filter_by(product_id=product_id).first()

    # 判断买家和商品是否存在
    if not buyer or not product:
        return jsonify({"error": "Buyer or product not found"}), 404

    # 判断商品库存是否足够
    if product.storage < quantity:
        return jsonify({"success": False, "error": "Not enough stock"}), 400

    total_price = product.price * quantity

    # 判断买家账户的钱是否足够
    if buyer.balance < total_price:
        return jsonify({"success": False, "error": "Insufficient funds"}), 400

    # balance减少，storage减少，新的purchase添加到数据库中
    buyer.balance -= total_price
    product.storage -= quantity

    new_purchase = Purchase(
        product_id=product.product_id,
        buyer_phone=buyer.phone,
        purchase_number=quantity,
        purchase_price=total_price,
        purchase_time=datetime.now(),
        image_src_at_time_of_purchase=product.image_src
    )

    db.session.add(new_purchase)
    db.session.commit()

    # logging.debug("buyItem finished.")
    return jsonify({"success": True}), 200

@buyer_bp.route('/getMoney', methods=['GET'])
def get_money():
    phone = request.args.get('phone')

    # 验证 phone 是否存在
    if not phone:
        return jsonify({"error": "手机号不能为空"}), 400

    buyer = Buyer.query.filter_by(phone=phone).first()

    # 判断买家是否存在
    if not buyer:
        return jsonify({"error": "买家不存在"}), 404

    # 返回买家的余额
    return jsonify({"phone": phone, "money": buyer.balance}), 200



@buyer_bp.route('/modifyBuyerInfo', methods=['POST'])
def modify_buyer_info():
    phone = request.json.get('phone')
    name = request.json.get('name')
    introduction = request.json.get('introduction')
    password = request.json.get('password')

    # 验证 phone 是否存在
    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    buyer = Buyer.query.filter_by(phone=phone).first()
    if not buyer:
        return jsonify({"error": "Buyer not found"}), 404

    # 更新信息
    if name:
        buyer.name = name
    if introduction:
        buyer.description = introduction
    if password:
        # 加密
        hashed_password = generate_password_hash(password)
        buyer.user.password = hashed_password

    db.session.commit()
    return jsonify({"message": "Buyer information updated successfully"}), 200

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
            # name = user.seller.name
            name = ""
        else:
            # name = None
            name = ""
    elif user.user_type == '1':  # 买家
        if user.buyer:
            name = user.buyer.name
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

