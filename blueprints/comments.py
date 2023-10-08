from flask import Blueprint, jsonify, request
from models import Comment, Buyer, db, Product

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

@comment_bp.route('/createComment', methods=['GET'])
def create_comment():
    buyer_phone = request.args.get('buyer_phone')
    content = request.args.get('content')

    try:
        rating = int(request.args.get('rating'))
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. Rating and Product ID should be integers."}), 400

    # 验证买家是否存在
    buyer = Buyer.query.filter_by(phone=buyer_phone).first()
    if not buyer:
        return jsonify({"message": "Buyer not found!"}), 400

    # 创建新的评论 (用这种方法来是comment插入数据库中)
    comment = Comment(
        content=content,
        rating=rating,
        product_id=product_id,
        buyer_phone=buyer_phone
    )

    # 将评论添加到数据库
    db.session.add(comment)
    db.session.commit()

    # 状态码201表示创建成功
    return jsonify({"message": "Comment added successfully!"}), 201


@comment_bp.route('/commentBasicInfoById', methods=['GET'])
def comment_basic_info_by_id():
    product_id_data = request.args.get('product_id')

    # product_id是否存在; 是否为整数
    try:
        product_id = int(product_id_data)
    except (TypeError, ValueError):
        # return jsonify({"error": "Invalid Product ID. Please provide a valid integer."}), 400
        return jsonify([])

    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        # return jsonify({"error": "Product not found"}), 404
        return jsonify([])

    # 获取最高的5个评论
    top_comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.desc()).limit(5).all()

    # 获取最低的5个评论
    bottom_comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.asc()).limit(5).all()

    # top5 + 低5
    combined_comments = top_comments + bottom_comments

    comments_data = []
    for comment in combined_comments:
        buyer = Buyer.query.filter_by(phone=comment.buyer_phone).first()
        comments_data.append({
            "user_name": buyer.name,
            "content": comment.content,
            "rating": comment.rating
        })

    return jsonify(comments_data), 200


@comment_bp.route('/commentInfoById', methods=['GET'])
def comment_info_by_id():
    product_id_data = request.args.get('product_id')
    buyer_phone_data = request.args.get('buyer_phone')

    # 检查product_id和buyer_phone是否存在
    try:
        product_id = int(product_id_data)
    except (TypeError, ValueError):
        # return jsonify({"error": "Invalid Product ID. Please provide a valid integer."}), 400
        return jsonify([])
    # 检查买家是否存在
    buyer = Buyer.query.filter_by(phone=buyer_phone_data).first()
    if not buyer:
        # return jsonify({"error": "Buyer not found"}), 404
        return jsonify([])
    # 查询与该商品和买家相关的评论
    comment = Comment.query.filter_by(product_id=product_id, buyer_phone=buyer.phone).first()
    if not comment:
        # return jsonify({"error": "Comment not found"}), 404
        return jsonify([])
    comment_data = {
        "user_name": buyer.name,
        "content": comment.content,
        "rating": comment.rating
    }

    return jsonify(comment_data), 200




