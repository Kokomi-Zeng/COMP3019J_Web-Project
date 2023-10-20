# blueprints/image.py

from flask import Blueprint, request, jsonify
import requests
from exts import db
from models import Product, User

image_bp = Blueprint('image', __name__, url_prefix='/images')

API_ENDPOINT = 'https://pinoss.com/kokomi/api/upload/'
API_TOKEN = '1986648502b84b6b7114'

@image_bp.route('/upload_image_product', methods=['POST'])
def upload_image_for_product():
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


@image_bp.route('/upload_image_user', methods=['POST'])
def upload_image_for_user():
    uploaded_file = request.files['image']
    phone = request.form.get('phone')  # 获取表单中的phone

    # 验证用户手机号是否存在
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"})

    files = {
        'uploadedFile': (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)
    }
    data = {
        'api_token': API_TOKEN,
        'upload_format': 'file'
    }

    response = requests.post(API_ENDPOINT, files=files, data=data).json()

    if response['status'] == 'success':
        user.image_src = response['url']  # 更新用户的image_src字段
        db.session.commit()
        return jsonify({"success": True, "message": "Image uploaded and saved successfully!", "url": response['url']})
    else:
        return jsonify({"success": False, "message": "Error during image upload"})


@image_bp.route('/get_image_product/', methods=['GET'])
def get_image_from_product():
    product_id = request.args.get('product_id')

    if not product_id:
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

@image_bp.route('/get_image_user', methods=['GET'])
def get_image_from_user():
    phone = request.args.get('phone')

    if not phone:
        return jsonify({"success": False, "message": "Phone number is required", "url": ""})

    # 根据phone查询用户
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return jsonify({"success": False, "message": "User not found", "url": ""})
    if not user.image_src:
        return jsonify({"success": False, "message": "Image not found for the specified user", "url": ""})
    return jsonify({"success": True, "message": "Image retrieved successfully", "url": user.image_src})






