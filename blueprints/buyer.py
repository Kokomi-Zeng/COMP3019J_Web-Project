from flask import Blueprint, render_template, request, jsonify

from models import Product, Comment

buyer_bp = Blueprint('buyer', __name__, url_prefix='/buyer')

@buyer_bp.route('/products')
def product_list():
    return render_template('buyer_product_list.html')

@buyer_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    return render_template('product_detail.html', product_id=product_id)

@buyer_bp.route('/product/<int:product_id>/leave_review')
def leave_review(product_id):
    return render_template('leave_review.html', product_id=product_id)

@buyer_bp.route('/product/<int:product_id>/purchase')
def purchase_product(product_id):
    return render_template('purchase_product.html', product_id=product_id)



@buyer_bp.route('/search', methods=['GET'])
def search():
    # 从查询字符串中尝试获取 keyword 参数的值，如果不存在，则返回空字符串
    keyword = request.args.get('keyword', '')  # 获取 URL 中的查询参数
    # 使用 SQLAlchemy 的 ilike 进行模糊搜索
    products = Product.query.filter(Product.product_name.ilike(f"%{keyword}%")).all()
    products_list = [{"product_name": product.product_name} for product in products]
    return jsonify(products=products_list)


@buyer_bp.route("/products/five-stars", methods=["GET"])
def five_star_products():
    # 查询评级为5的评论相关的所有商品
    five_star_reviews = Comment.query.filter_by(rating=5).all()

    # 使用集合来确保商品不重复
    products = {comment.product for comment in five_star_reviews}
    products_list = [{"product_id": product.product_id} for product in products]

    return jsonify(products_list)


