from flask import Blueprint, render_template, session, jsonify, request
from models import User

"""
The following code is used to store the routes related to index,
such as getAuthorizePage, getLoginPage, getSellerInfo, getShopPage, getRegisterPage, getBuyerInfoPage, getItemPage, getSession, clearSession.
"""

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/authorize')
def getAuthorizePage():
    mode_info = get_mode_info()

    return render_template('authorize.html', **mode_info)


@bp.route('/login')
def getLoginPage():
    user_info = get_user_info()
    mode_info = get_mode_info()

    return render_template('login.html', **user_info, **mode_info)


@bp.route('/buyerItem')
def getSellerInfo():
    user_info = get_user_info()
    mode_info = get_mode_info()

    return render_template('buyerItem.html', **user_info, **mode_info)

@bp.route('/shop')
@bp.route('/')
def getShopPage():
    user_info = get_user_info()
    mode_info = get_mode_info()

    return render_template('shop.html', **user_info, **mode_info)


@bp.route('/register')
def getRegisterPage():
    user_info = get_user_info()
    mode_info = get_mode_info()

    return render_template('register.html', **user_info, **mode_info)


@bp.route('/buyerInfo')
def getBuyerInfoPage():
    user_info = get_user_info()
    mode_info = get_mode_info()

    return render_template('buyerInfo.html', **user_info, **mode_info)

@bp.route('/sellerInfo')
def getSellerInfoPage():
    user_info = get_user_info()
    mode_info = get_mode_info()


    return render_template('sellerInfo.html', **user_info, **mode_info)


@bp.route('/admin')
def getAdminPage():
    user_info = get_user_info()
    mode_info = get_mode_info()


    return render_template('admin.html', **user_info, **mode_info)


@bp.route('/item')
def getItemPage():
    product_info = get_product_id()
    mode_info = get_mode_info()


    return render_template("item.html", **product_info, **mode_info)

@bp.route('/itemSeller')
def getItemSellerPage():
    product_info = get_product_id()
    mode_info = get_mode_info()


    return render_template("itemSeller.html", **product_info, **mode_info)

@bp.route('/itemBuyer')
def getItemBuyerPage():
    product_info = get_product_id()
    mode_info = get_mode_info()


    return render_template("itemBuyer.html", **product_info, **mode_info)

@bp.route('/comment')
def getCommentPage():
    product_info = get_product_id()
    mode_info = get_mode_info()


    return render_template("comment.html", **product_info, **mode_info)


# Admin


@bp.route('/buyerManage')
def getBuyerManagePage():
    phone = request.args.get('phone')
    mode_info = get_mode_info()


    return render_template('buyerManage.html', phone=phone, **mode_info)

@bp.route('/sellerManage')
def getSellerManagePage():
    phone = request.args.get('phone')
    mode_info = get_mode_info()


    return render_template('sellerManage.html', phone=phone, **mode_info)

@bp.route('/itemManage')
def getItemManagePage():
    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    mode_info = get_mode_info()


    return render_template('itemManage.html', product_id=product_id, **mode_info)

@bp.route('/buyerItemManage')
def getBuyerItemManagePage():
    phone = request.args.get('phone')

    mode_info = get_mode_info()
    return render_template('buyerItemManage.html', phone=phone, **mode_info)


@bp.route('/sellerAdd')
def getSellerAddPage():
    user_info = get_user_info()

    mode_info = get_mode_info()
    return render_template('sellerAdd.html', **user_info, **mode_info)

# This route is used to get the session
@bp.route('/getSession')
def getSession():
    phone = session.get('phone')
    # If there is no "phone" on the session
    if not phone:
        return {'phone': "", 'name': "", 'type': "", 'status': ""}
    user = User.query.get(phone)
    if user:
        if user.user_type == '0':
            return {'phone': phone, 'name': user.seller.name, 'type': user.user_type, 'status': user.status}
        if user.user_type == '1':
            return {'phone': phone, 'name': user.buyer.name, 'type': user.user_type, 'status': user.status}
        if user.user_type == '2':
            return {'phone': phone, 'name': "administer", 'type': user.user_type, 'status': user.status}
    else:
        return {'phone': "", 'name': "", 'type': ""}


# This route is used to clear the session
@bp.route('/clearSession')
def clearSession():
    session.clear()
    return {'success': True}


def get_mode_info():
    user_mode = session.get('mode', '')
    if user_mode:
        user_mode = ''
    else:
        user_mode = 'dark-mode'
    return {'user_mode': user_mode}


# This route is used to get the user info
def get_user_info():
    phone = session.get('phone')

    # first to determine if there is a phone in the session, if not, return None
    if not phone:
        return {
            'phone': "",
            'name': "",
            'type': ""
        }

    # If there is a phone, but the user is not in the database, return None
    user = User.query.get(phone)
    if not user:
        return {
            'phone': "",
            'name': "",
            'type': ""
        }

    # Get the name according to the user type, the "if judgment" inside is to prevent the program from
    # reporting an error due to the lack of information of the user in the database
    if user.user_type == '0':  # seller
        if user.seller:
            name = user.seller.name
        else:
            name = ""
    elif user.user_type == '1':  # buyer
        if user.buyer:
            name = user.buyer.name
        else:
            name = ""
    else:
        name = ""

    # Determine whether the name is an empty string (a non-registered user)
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


# This route is used to get the product ID
def get_product_id():
    # If the product ID type is wrong
    try:
        product_id = int(request.args.get('product_id'))
    except(TypeError, ValueError):
        return {"success": False, "message": "Wrong product ID type"}

    return {"success": True, "product_id": product_id}
