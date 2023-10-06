from flask import Blueprint, jsonify, request
from models import Comment, Buyer, db

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

@comment_bp.route('/createComment', methods=['POST'])
def create_comment():
    phone = request.json.get('phone')
    content = request.json.get('content')
    rating = int(request.json.get('rating'))
    product_id = int(request.json.get('product_id'))

    # 验证买家是否存在
    buyer = Buyer.query.filter_by(phone=phone).first()
    if not buyer:
        return jsonify({"message": "Buyer not found!"}), 400

    # 创建新的评论 (用这种方法来是comment插入数据库中)
    comment = Comment(
        content=content,
        rating=rating,
        product_id=product_id,
        buyer_phone=phone
    )

    # 将评论添加到数据库
    db.session.add(comment)
    db.session.commit()

    # 状态码201表示创建成功
    return jsonify({"message": "Comment added successfully!"}), 201

