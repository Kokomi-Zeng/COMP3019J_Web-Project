from flask import jsonify, request

from models import Product

# @app.route('/get-products', methods=['GET'])
def get_products():
    # 使用request.args.get从请求的URL参数中获取页码page。如果该参数不存在，它会默认为1。type=int确保返回的是整数类型。
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = Product.query.paginate(page, per_page=per_page, error_out=False)

    # 获取当前页上的所有商品。它是一个商品对象的列表
    products = pagination.items

    # 将数据转换为可以JSON化的格式
    products_data = [{"id": product.id} for product in products]

    return jsonify({
        'products': products_data,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'next_num': pagination.next_num,
        'prev_num': pagination.prev_num
    })
