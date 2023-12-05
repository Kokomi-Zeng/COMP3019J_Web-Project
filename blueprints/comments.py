from flask import Blueprint, jsonify, request, render_template
from models import Comment, Buyer, db, Product, User

"""
The following code is used to store the routes related to comment,
such as createComment, commentBasicInfoById, commentInfoById, hasNextComment, getIntroductionByCommentID.
"""

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')


# Provide create comment method for a buyer to create a comment
@comment_bp.route('/createComment', methods=['GET'])
def create_comment():
    commenter_phone = request.args.get('buyer_phone')
    content = request.args.get('content')

    try:
        rating = int(request.args.get('rating'))
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid input. Rating and Product ID should be integers."})

    # verify if the buyer exists
    buyer = Buyer.query.filter_by(phone=commenter_phone).first()
    if not buyer:
        return jsonify({"success": False, "message": "Buyer(Commenter) not found!"})

    # if the rating is not 1 or 2 or 3 or 4 or 5
    if not (rating == 1 or rating == 2 or rating == 3 or rating == 4 or rating == 5):
        return jsonify({"success": False, "message": "Rating must be 1 or 2 or 3 or 4 or 5"})

    # if the buyer enter an empty comment or None
    if content is None or content == "" or content == "None":
        return jsonify({"success": False, "message": "Comment can't be empty or None"})

    # create a new comment
    comment = Comment(
        content=content,
        rating=rating,
        product_id=product_id,
        commenter_phone=commenter_phone
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({"success": True, "message": "Comment added successfully!"})


# Provide get comment basic info by product id method for a non-login user to get the basic info of comments
@comment_bp.route('/commentBasicInfoById', methods=['GET'])
def comment_basic_info_by_id():
    product_id_data = request.args.get('product_id')

    # If product_id exists; If product_id is an integer
    try:
        product_id = int(product_id_data)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    # get the top 5 comments
    top_comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.desc()).limit(5).all()

    # get the bottom 5 comments
    bottom_comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.asc()).limit(5).all()

    # use set operation to remove duplicate comments
    combined_comments = list(set(top_comments + bottom_comments))

    # rank the comments from high to low
    combined_comments.sort(key=lambda x: x.rating, reverse=True)

    comments_data = []
    for comment in combined_comments:
        # 评论人名字
        buyer = Buyer.query.filter_by(phone=comment.commenter_phone).first()
        user_commenter = User.query.filter_by(phone=comment.commenter_phone).first()

        comments_data.append({
            "commenter_name": buyer.name,
            "user_image": user_commenter.image_src,
            "content": comment.content,
            "rating": comment.rating,
            "comment_id": comment.comment_id,
        })

    return jsonify(comments_data)


# Provide get comment info by product id method for a login user to get the info of comments
@comment_bp.route('/commentInfoById', methods=['GET'])
def comment_info_by_id():
    product_id_data = request.args.get('product_id')
    phone_data = request.args.get('phone')

    # verify if the product_id and page_num are integers
    try:
        product_id = int(product_id_data)
        page_num_data = request.args.get('page_num', default=1, type=int)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID or Page Number. Please provide a valid integer."})

    # if page_num is less than 1
    if page_num_data < 1:
        return jsonify({"success": False, "message": "Page Number must be greater than 0"})

    #
    user = User.query.filter_by(phone=phone_data).first()

    if not user:
        return jsonify({"success": False, "message": "Buyer or seller not found"})

    # set the number of comments per page
    per_page = 10
    # set the start index and end index of the comments
    start_idx = (page_num_data - 1) * per_page
    end_idx = start_idx + per_page

    # query the comments and sort them from high to low
    comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.rating.desc()).all()
    # comments = comments[start_idx:end_idx]

    if not comments:
        return jsonify({"success": False, "message": "Comment not found"})

    comments_data = []
    for comment in comments:
        buyer = Buyer.query.filter_by(phone=comment.commenter_phone).first()
        user_commenter = User.query.filter_by(phone=comment.commenter_phone).first()
        comments_data.append({
            "comment_id": comment.comment_id,
            "commenter_name": buyer.name,
            "content": comment.content,
            "rating": comment.rating,
            "user_image": user_commenter.image_src,
        })

    return jsonify(comments_data)


# Provide has next comment method for a login user to check if there is a next page of comments
@comment_bp.route('/hasNextComment', methods=['GET'])
def has_next_comment():
    product_id_data = request.args.get('product_id')
    phone_data = request.args.get('phone')

    # check if product_id and page_num are integers
    try:
        product_id = int(product_id_data)
        page_num_data = request.args.get('page_num', default=1, type=int)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID or Page Number. Please provide a valid integer."})

    # check if page_num is less than 1
    if page_num_data < 1:
        return jsonify({"success": False, "message": "Page Number must be greater than 0"})

    user = User.query.filter_by(phone=phone_data).first()

    if not user:
        return jsonify({"success": False, "message": "Buyer or seller not found"})

    # query the total number of comments
    total_comments = Comment.query.filter_by(product_id=product_id).count()

    # check if there is a next page
    if total_comments > page_num_data * 10:
        return jsonify({"success": True, "message": "Has next comment"})
    else:
        return jsonify({"success": False, "message": "No next comment"})


# Provide get introduction by comment id method for a  user to get the introduction of the buyer who commented this product
@comment_bp.route('/getIntroductionByCommentID', methods=['GET'])
def get_introduction_by_comment_id():
    comment_id_data = request.args.get('comment_id')

    # check if comment_id is an integer
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

@comment_bp.route('/getALlComments', methods=['GET'])
def get_all_comments():
    comments = Comment.query.all()
    comments_data = []
    for comment in comments:
        buyer = Buyer.query.filter_by(phone=comment.commenter_phone).first()
        user_commenter = User.query.filter_by(phone=comment.commenter_phone).first()
        comments_data.append({
            "comment_id": comment.comment_id,
            "commenter_name": buyer.name,
            "content": comment.content,
            "rating": comment.rating,
            "user_image": user_commenter.image_src,
        })

    return jsonify(comments_data)
