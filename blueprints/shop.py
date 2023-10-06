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



@shop_bp.route('/hasNextPage', methods=['GET'])
def has_next_page():




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




