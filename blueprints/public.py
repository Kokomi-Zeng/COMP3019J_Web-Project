from flask import Blueprint, render_template, request, jsonify
from models import Comment

# 游客访问的蓝图
public_bp = Blueprint('public', __name__)

def product_reviews(product_id):
    # 查询该商品的所有评论
    reviews = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.desc()).all()

    # 获取评级最高的前5条评论和评级最低的5条评论
    top_reviews = reviews[:5]
    bottom_reviews = reviews[-5:]

    # 将评论转换为字典列表
    top_reviews_list = [{"buyer": review.buyer_phone, "rating": review.rating, "content": review.content} for review in top_reviews]
    bottom_reviews_list = [{"buyer": review.buyer_phone, "rating": review.rating, "content": review.content} for review in bottom_reviews]

    return jsonify({"top_reviews": top_reviews_list, "bottom_reviews": bottom_reviews_list})