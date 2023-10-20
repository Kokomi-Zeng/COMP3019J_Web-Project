# blueprints/image.py

from flask import Blueprint, request, jsonify
import requests
from exts import db
from models import Product

image_bp = Blueprint('image', __name__, url_prefix='/images')

API_ENDPOINT = 'https://pinoss.com/kokomi/api/upload/'
API_TOKEN = '1986648502b84b6b7114'

@image_bp.route('/upload-to-pinoss', methods=['POST'])
def upload_image():
    uploaded_file = request.files['image']
    product_id = request.form.get('product_id')  # 获取表单中的product_id

    # 验证产品ID是否存在
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    files = {
        'uploadedFile': (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)
    }
    data = {
        'api_token': API_TOKEN,
        'upload_format': 'file'
    }

    response = requests.post(API_ENDPOINT, files=files, data=data).json()

    if response['status'] == 'success':
        product.image_src = response['url']  # 更新产品的image_src字段
        db.session.commit()
        return jsonify({"success": True, "message": "Image uploaded and saved successfully!", "url": response['url']})
    else:
        return jsonify({"success": False, "message": "Error during image upload"})


@image_bp.route('/get-image/', defaults={'product_id': None}, methods=['GET'])
@image_bp.route('/get-image/<int:product_id>', methods=['GET'])
def get_image(product_id):
    if product_id is None:
        return jsonify({"success": False, "message": "Product ID is required", "url": ""})

    # 验证产品ID是否为int
    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({"success": False, "message": "Product ID must be an integer", "url": ""})

    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"success": False, "message": "Product not found", "url": ""})
    if not product.image_src:
        return jsonify({"success": False, "message": "Image not found for the specified product", "url": ""})
    return jsonify({"success": True, "message": "Image retrieved successfully", "url": product.image_src})





