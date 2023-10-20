from flask import Blueprint, jsonify, request, render_template
from models import Comment, Buyer, db, Product, User

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

@comment_bp.route('/createComment', methods=['GET'])
def create_comment():
    commenter_phone = request.args.get('buyer_phone')
    content = request.args.get('content')

    try:
        rating = int(request.args.get('rating'))
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid input. Rating and Product ID should be integers."})

    # 验证买家是否存在
    buyer = Buyer.query.filter_by(phone=commenter_phone).first()
    if not buyer:
        return jsonify({"success": False, "message": "Buyer(Commenter) not found!"})

    if not (rating == 1 or rating == 2 or rating == 3 or rating == 4 or rating == 5):
        return jsonify({"success": False, "message": "Rating must be 1 or 2 or 3 or 4 or 5"})

    if content is None or content == "" or content == "None":
        return jsonify({"success": False, "message": "Comment can't be empty or None"})

    # 创建新的评论 (用这种方法来是comment插入数据库中)
    comment = Comment(
        content=content,
        rating=rating,
        product_id=product_id,
        commenter_phone=commenter_phone
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
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    # 获取最高的5个评论
    top_comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.desc()).limit(5).all()

    # 获取最低的5个评论
    bottom_comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.asc()).limit(5).all()

    # 使用集合运算去除重复评论
    combined_comments = list(set(top_comments + bottom_comments))

    # 将评论从评分高到低排序
    combined_comments.sort(key=lambda x: x.rating, reverse=True)

    comments_data = []
    for comment in combined_comments:
        # 评论人名字
        buyer = Buyer.query.filter_by(phone=comment.commenter_phone).first()
        comments_data.append({
            "commenter_name": buyer.name,
            "user_image": "",
            "content": comment.content,
            "rating": comment.rating,
            "comment_id": comment.comment_id,
        })

    return jsonify(comments_data)


@comment_bp.route('/commentInfoById', methods=['GET'])
def comment_info_by_id():
    product_id_data = request.args.get('product_id')
    phone_data = request.args.get('phone')

    # 检查product_id是否正确
    try:
        product_id = int(product_id_data)
        page_num_data = request.args.get('page_num', default=1, type=int)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID or Page Number. Please provide a valid integer."})

    if page_num_data < 1:
        return jsonify({"success": False, "message": "Page Number must be greater than 0"})

    user = User.query.filter_by(phone=phone_data).first()

    if not user:
        return jsonify({"success": False, "message": "Buyer or seller not found"})

    # 设置每页的评论数量
    per_page = 10
    start_idx = (page_num_data - 1) * per_page
    end_idx = start_idx + per_page

    # 查询评论,并按照评分从高到低排序
    comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.desc()).slice(start_idx, end_idx).all()

    if not comments:
        return jsonify({"success": False, "message": "Comment not found"})

    comments_data = []
    for comment in comments:
        buyer = Buyer.query.filter_by(phone=comment.commenter_phone).first()
        comments_data.append({
            "user_name": buyer.name,
            "content": comment.content,
            "rating": comment.rating
        })

    return jsonify(comments_data)

# comment是否有下一页
@comment_bp.route('/hasNextComment', methods=['GET'])
def has_next_comment():
    product_id_data = request.args.get('product_id')
    phone_data = request.args.get('phone')

    # 检查product_id是否正确
    try:
        product_id = int(product_id_data)
        page_num_data = request.args.get('page_num', default=1, type=int)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID or Page Number. Please provide a valid integer."})

    if page_num_data < 1:
        return jsonify({"success": False, "message": "Page Number must be greater than 0"})

    user = User.query.filter_by(phone=phone_data).first()

    if not user:
        return jsonify({"success": False, "message": "Buyer or seller not found"})

    # 查询评论的总数
    total_comments = Comment.query.filter_by(product_id=product_id).count()

    # 查看是否还有下一页
    if total_comments > page_num_data * 10:
        return jsonify({"success": True, "message": "Has next comment"})
    else:
        return jsonify({"success": False, "message": "No next comment"})

@comment_bp.route('/getIntroductionByCommentID', methods=['GET'])
def get_introduction_by_comment_id():
    comment_id_data = request.args.get('comment_id')

    # 检查comment_id是否正确
    try:
        comment_id = int(comment_id_data)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Comment ID. Please provide a valid integer."})

    comment = Comment.query.filter_by(comment_id=comment_id).first()
    if not comment:
        return jsonify({"success": False, "message": "Comment not found"})

    buyer = Buyer.query.filter_by(phone=comment.commenter_phone).first()
    if not buyer:
        return jsonify({"success": False, "message": "Buyer not found"})

    return jsonify({
        "head": "",
        "name": buyer.name,
        "introduction": buyer.description
    })
