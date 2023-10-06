from flask import Blueprint, render_template, session, request, jsonify

seller_bp = Blueprint('seller', __name__, url_prefix='/seller')

from models import Product, Comment, Buyer, User, Seller

@seller_bp.route('/')
def seller():
    user_info = get_user_info()

    # **user_info相当于phone=user_info['phone'], name=user_info['name'], type=user_info['type']
    return render_template('seller.html', **user_info)


@seller_bp.route('/buyerInfo', methods=['GET'])
def seller_info():
    phone = request.json.get('phone')

    # 假如没有传入phone，返回服务器200状态码，表示请求成功，但是没有数据
    if not phone:
        return jsonify({"data": None}), 200

    seller = Seller.query.filter_by(phone=phone).first()
    # 假如用户不存在，返回服务器200状态码，表示请求成功，但是没有数据
    if not seller:
        return jsonify({"data": None}), 200

    return jsonify({
        "phone": seller.phone,
        # 事实上，这里不能返回密码，因为密码是加密的，除非不让加密，但这不合理，建议直接不显示得了
        # "password": seller.user.password,
        "name": seller.name,
        "introduction": seller.description,
    })



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
            # 这个先这么放着，等会儿再改
            name = None
        else:
            name = None
    else:
        name = None

    return {
        'phone': phone,
        'name': name,
        'type': user.user_type
    }
