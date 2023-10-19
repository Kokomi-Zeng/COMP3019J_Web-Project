from flask import Blueprint, jsonify, request, render_template
from models import Comment, Buyer, db, Product, User

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

@comment_bp.route('/')
def comment():
    return render_template('comment.html')


@comment_bp.route('/createComment', methods=['GET'])
def create_comment():
    buyer_phone = request.args.get('buyer_phone')
    content = request.args.get('content')

    try:
        rating = int(request.args.get('rating'))
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid input. Rating and Product ID should be integers."})

    # 验证买家是否存在
    buyer = Buyer.query.filter_by(phone=buyer_phone).first()
    if not buyer:
        return jsonify({"success": False, "message": "Buyer not found!"})

    if not (rating == 1 or rating == 2 or rating == 3 or rating == 4 or rating == 5):
        return jsonify({"success": False, "message": "Rating must be 1 or 2 or 3 or 4 or 5"})

    if content is None or content == "":
        return jsonify({"success": False, "message": "Comment can't be empty"})

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
    return jsonify({"success": True, "message": "Comment added successfully!"})


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

    # 使用集合运算去除重复评论
    combined_comments = list(set(top_comments + bottom_comments))

    comments_data = []
    for comment in combined_comments:
        buyer = Buyer.query.filter_by(phone=comment.buyer_phone).first()
        comments_data.append({
            "user_name": buyer.name,
            "content": comment.content,
            "rating": comment.rating
        })

    return jsonify(comments_data)


@comment_bp.route('/commentInfoById', methods=['GET'])
def comment_info_by_id():
    product_id_data = request.args.get('product_id')
    phone_data = request.args.get('phone')

    # 检查product_id是否正确
    try:
        product_id = int(product_id_data)
    except (TypeError, ValueError):
        # return jsonify({"error": "Invalid Product ID. Please provide a valid integer."}), 400
        return jsonify([])

    user = User.query.filter_by(phone=phone_data).first()

    if not user:
        # return jsonify({"error": "Buyer not found"}), 404
        return jsonify([])

    # 查询评论
    comment = Comment.query.filter_by(product_id=product_id).first()

    if not comment:
        # return jsonify({"error": "Comment not found"}), 404
        return jsonify([])


    # 查询这个商品对应的买家
    buyer = Buyer.query.filter_by(phone=comment.buyer_phone).first()
    comment_data = {
        "user_name": buyer.name,
        "content": comment.content,
        "rating": comment.rating
    }

    return jsonify(comment_data)

# 辅助函数来计算商品的平均rating



