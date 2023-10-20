from flask import Blueprint, render_template, session, jsonify, request
from models import User

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/authorize')
def getAuthorizePage():
    return render_template('authorize.html')


@bp.route('/login')
def getLoginPage():
    user_info = get_user_info()
    return render_template('login.html', **user_info)


@bp.route('/sellerInfo')
def getSellerInfo():
    user_info = get_user_info()
    return render_template('sellerInfo.html', **user_info)


@bp.route('/shop')
@bp.route('/')
def getShopPage():
    user_info = get_user_info()
    return render_template('shop.html', **user_info)


@bp.route('/register')
def getRegisterPage():
    user_info = get_user_info()
    return render_template('register.html', **user_info)


@bp.route('/buyerInfo')
def getBuyerInfoPage():
    user_info = get_user_info()
    return render_template('buyerInfo.html', **user_info)


@bp.route('/item')
def getItemPage():
    product_info = get_product_id()
    return render_template("item.html", **product_info)


@bp.route('/getSession')
def getSession():
    phone = session.get('phone')
    user = User.query.get(phone)
    if user:
        if user.user_type == '0':
            return {'phone': phone, 'name': user.seller.name, 'type': user.user_type}
        if user.user_type == '1':
            return {'phone': phone, 'name': user.buyer.name, 'type': user.user_type}
    else:
        return {'phone': "", 'name': "", 'type': ""}


# 清除session (clear session)
@bp.route('/clearSession')
def clearSession():
    session.clear()
    return {'success': True}



def get_user_info():
    phone = session.get('phone')

    # 先判断session中是否有phone，如果没有，返回None
    if not phone:
        return {
            'phone': "",
            'name': "",
            'type': ""
        }

    # 如果有phone，但是数据库中没有该用户，返回None
    user = User.query.get(phone)
    if not user:
        return {
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


def get_product_id():
    # 如果商品ID类型错误
    try:
        product_id = int(request.args.get('product_id'))
    except(TypeError, ValueError):
        return {"success": False, "message": "Wrong product ID type"}

    return {"success": True, "product_id": product_id}
