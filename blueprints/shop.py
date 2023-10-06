from flask import Blueprint, render_template, session, request, jsonify
from models import User, Product, Comment
from sqlalchemy import func
from exts import db

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')


@shop_bp.route('/')
def shop():
    user_info = get_user_info()

    # **user_info相当于phone=user_info['phone'], name=user_info['name'], type=user_info['type']
    return render_template('shop.html', **user_info)


@shop_bp.route('/searchItemByName', methods=['GET'])
def search_item_by_name():
    phone = request.json.get('phone')
    keyword = request.json.get('keyword')
    page_num = int(request.json.get('page_num'))

    # 如果关键词存在并且不为空格
    if keyword and keyword.strip():
        # error_out=False表示如果页数超出范围，不会报错，而是返回空列表
        items = Product.query.filter(Product.product_name.contains(keyword)).paginate(page=page_num, per_page=10, error_out=False)
    # 如果关键词为空或只有空格
    else:
        items = Product.query.paginate(page=page_num, per_page=10, error_out=False)

    results = [{"product_name": item.product_name, "product_id": item.product_id} for item in items.items]
    return jsonify(results)



@shop_bp.route('/hasNextPage', methods=['GET'])
def has_next_page():
    phone = request.json.get('phone')
    keyword = request.json.get('keyword')
    page_num = int(request.json.get('page_num'))

    if keyword and keyword.strip():
        items = Product.query.filter(Product.product_name.contains(keyword)).paginate(page=page_num, per_page=10, error_out=False)
    else:
        items = Product.query.paginate(page=page_num, per_page=10, error_out=False)

    return jsonify({"has_next": items.has_next})


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




