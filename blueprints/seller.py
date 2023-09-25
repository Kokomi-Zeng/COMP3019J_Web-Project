from flask import Blueprint, render_template

seller_bp = Blueprint('seller', __name__, url_prefix='/seller')

@seller_bp.route('/upload')
def upload_product():
    return render_template('upload_product.html')

@seller_bp.route('/products')
def product_list():
    return render_template('seller_product_list.html')

@seller_bp.route('/product/<int:product_id>/reviews')
def product_reviews(product_id):
    return render_template('product_reviews.html', product_id=product_id)
