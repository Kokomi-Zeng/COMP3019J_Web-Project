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
    phone = request.args.get('phone')
    # 没输keyword，等于输了空格
    keyword = request.args.get('keyword', '')

    try:
        page_num = int(request.args.get('page_num', 1))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid page number"}), 400

    per_page = 10
    # offset是从第几个开始，limit是取多少个
    offset = (page_num - 1) * per_page

    # 找到用户
    user = User.query.filter_by(phone=phone).first()
    query = Product.query

    # 如果keyword不为空
    if keyword:
        # 这实际上是买家和游客的搜索结果
        query = query.filter(Product.product_name.like(f"%{keyword}%"))

    # 如果是买家或卖家(user存在)
    if user:
        # 如果是卖家
        if user.user_type == "0":
            # 只能搜索自己的商品
            query = query.filter_by(seller_phone=phone)
    # 如果是游客，限制你翻页
    else:
        if page_num > 1:
            return jsonify({"error": "Unauthorized access"}), 401

    # 某一页的全部商品
    products = query.limit(per_page).offset(offset).all()

    # 按照平均rating从高到低排序
    sorted_products = sorted(products, key=lambda product: calculate_average_rating(product.product_id), reverse=True)

    product_list = []
    for product in sorted_products:
        avg_rating = calculate_average_rating(product.product_id)
        product_list.append({
            "product_name": product.product_name,
            "image_src": product.image_src,
            "rating": avg_rating,
            "price": product.price,
            "product_id": product.product_id
        })

    return jsonify(product_list), 200




@shop.route('/hasNextPage', methods=['GET'])
def has_next_page():
    phone = request.args.get('phone')
    keyword = request.args.get('keyword', "")

    try:
        page_num = int(request.args.get('page_num', 1))
    except ValueError:
        return jsonify({"error": "Invalid page number"}), 400

    per_page = 10

    # 当前页之后的下一页还有多少个商品
    offset = page_num * per_page

    # 找到用户
    user = User.query.filter_by(phone=phone).first()
    query = Product.query

    if keyword:
        query = query.filter(Product.product_name.like(f"%{keyword}%"))

    if user:
        if user.user_type == "0":

            query = query.filter_by(seller_phone=phone)
    else:
        if page_num > 1:
            return jsonify({"error": "Unauthorized access"}), 401

    # offset: 从第几个开始，limit: 取多少个, count: 一共有多少个
    next_page_products_count = (query.limit(per_page).offset(offset)).count()
    boolean = next_page_products_count > 0
    return jsonify({"has_next": boolean})


# 辅助函数来计算商品的平均rating
def calculate_average_rating(product_id):
    comments = Comment.query.filter_by(product_id=product_id).all()
    # 如果没有评论，直接0.0分
    if not comments:
        return 0.0

    total_rating = 0
    for comment in comments:
        total_rating += comment.rating

    average_rating = total_rating / len(comments)
    return average_rating


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




