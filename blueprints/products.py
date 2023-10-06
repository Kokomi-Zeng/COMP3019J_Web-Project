from flask import Blueprint, jsonify, request
from models import Product, db

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/modifyItem', methods=['POST'])
def modify_item():
    product_id = request.form.get('product_id')
    seller_phone = request.form.get('seller_phone')
    price = float(request.form.get('price'))
    image_src = request.form.get('image_src')
    storage = int(request.form.get('storage'))
    product_name = request.form.get('product_name')
    description = request.form.get('description')

    # 验证商品是否存在
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # 检查商品是否属于该卖家
    if product.seller_phone != seller_phone:
        return jsonify({"message": "Unauthorized"}), 403

    # 更改商品信息
    product.price = price
    product.image_src = image_src
    product.storage = storage
    product.product_name = product_name
    product.description = description

    # 弄到数据库中
    db.session.commit()

    # 状态码200表示服务器已成功处理了请求
    return jsonify({"message": "Product updated successfully"}), 200

@products_bp.route('/addItem', methods=['POST'])
def add_item():
    seller_phone = request.form.get('seller_phone')
    price = float(request.form.get('price'))
    image_src = request.form.get('image_src')
    storage = int(request.form.get('storage'))
    product_name = request.form.get('product_name')
    description = request.form.get('description')

    # 创建新的商品
    product = Product(
        price=price,
        image_src=image_src,
        storage=storage,
        product_name=product_name,
        description=description,
        seller_phone=seller_phone
    )

    # 将商品添加到数据库
    db.session.add(product)
    db.session.commit()

    # 状态码201表示请求成功并且服务器创建了新的资源
    return jsonify({"message": "Product added successfully"}), 201


@products_bp.route('/deleteItem', methods=['POST'])
def delete_item():
    product_id = request.form.get('product_id')
    seller_phone = request.form.get('seller_phone')

    # 验证商品是否存在
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # 检查商品是否属于该卖家
    if product.seller_phone != seller_phone:
        return jsonify({"message": "Unauthorized"}), 403

    # 删除商品
    db.session.delete(product)
    db.session.commit()

    # 状态码200表示服务器已成功处理了请求
    return jsonify({"message": "Product deleted successfully"}), 200



