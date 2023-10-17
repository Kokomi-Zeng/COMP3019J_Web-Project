from flask import Blueprint, jsonify, request, render_template, session
from models import Product, db, Comment, User

test_bp = Blueprint('test', __name__, url_prefix='/')

@test_bp.route('/')
def getLoginPage():
    user_info = get_user_info()
    return render_template('login.html', **user_info)

@test_bp.route('/sellerInfo')
def getSellerInfo():
    user_info = get_user_info()
    return render_template('sellerInfo.html', **user_info)

@test_bp.route('/shop')
def getShopPage():
    user_info = get_user_info()
    return render_template('shop.html', **user_info)


@test_bp.route('/register')
def getRegisterPage():
    user_info = get_user_info()
    return render_template('register.html', **user_info)

@test_bp.route('/buyerInfo')
def getBuyerInfoPage():
    user_info = get_user_info()
    return render_template('buyerInfo.html', **user_info)

@test_bp.route('/item/<product_id>/<belong>')
def getItemPage(product_id, belong):
    return render_template("item.html", belong=belong, product_id=product_id)

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
