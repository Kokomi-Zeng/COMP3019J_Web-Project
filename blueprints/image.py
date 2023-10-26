# blueprints/image.py

from flask import Blueprint, request, jsonify
import requests
from exts import db
from models import Product, User

"""
The following code is used to store the routes related to image,
such as uploadImageForProduct, uploadImageForUser, getImageFromProduct, getImageFromUser.
"""

image_bp = Blueprint('image', __name__, url_prefix='/images')

# here is the API endpoint and token for the image upload service
API_ENDPOINT = 'https://pinoss.com/kokomi/api/upload/'
API_TOKEN = '1986648502b84b6b7114'


# Provide upload image for product method for a seller to upload image for a product
@image_bp.route('/upload_image_product', methods=['POST'])
def upload_image_for_product():
    uploaded_file = request.files['image']
    # get the product_id from the form
    product_id = request.args.get('product_id')
    print(product_id);

    # verify if the product exists
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"success": False, "message": "Product not found", "url": "https://pinoss.com/kokomi/i/2023/10/20/Product_Not_Found.png"})

    # upload the image to the image upload service use the requests library
    files = {
        'uploadedFile': (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)
    }
    data = {
        'api_token': API_TOKEN,
        'upload_format': 'file'
    }

    # get the response from the image upload service
    response = requests.post(API_ENDPOINT, files=files, data=data).json()

    # if the image upload service return success
    if response['status'] == 'success':
        # update the image_src field of the product
        product.image_src = response['url']
        db.session.commit()
        return jsonify({"success": True, "message": "Image uploaded and saved successfully!", "url": response['url']})
    else:
        return jsonify({"success": False, "message": "Error during image upload", "url": "https://pinoss.com/kokomi/i/2023/10/20/Product_Not_Found.png"})


# Provide upload image for user method for a user to upload image for himself/herself
@image_bp.route('/upload_image_user', methods=['POST'])
def upload_image_for_user():
    uploaded_file = request.files['image']
    phone = request.form.get('phone')

    # verify if the user exists
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return jsonify({"success": False, "message": "User not found", "url": "https://pinoss.com/kokomi/i/2023/10/20/default_image.jpg"})

    files = {
        'uploadedFile': (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)
    }
    data = {
        'api_token': API_TOKEN,
        'upload_format': 'file'
    }

    response = requests.post(API_ENDPOINT, files=files, data=data).json()

    if response['status'] == 'success':
        # update the image_src field of the user
        user.image_src = response['url']
        db.session.commit()
        return jsonify({"success": True, "message": "Image uploaded and saved successfully!", "url": response['url']})
    else:
        return jsonify({"success": False, "message": "Error during image upload", "url": "https://pinoss.com/kokomi/i/2023/10/20/default_image.jpg"})


# Provide get image from product method for a user to get the image of a product
@image_bp.route('/get_image_product/', methods=['GET'])
def get_image_from_product():
    product_id = request.args.get('product_id')

    if not product_id:
        return jsonify({"success": False, "message": "Product ID is required", "url": "https://pinoss.com/kokomi/i/2023/10/20/Product_Not_Found.png"})

    # verify if the product_id is an integer
    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({"success": False, "message": "Product ID must be an integer", "url": "https://pinoss.com/kokomi/i/2023/10/20/Product_Not_Found.png"})

    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"success": False, "message": "Product not found", "url": "https://pinoss.com/kokomi/i/2023/10/20/Product_Not_Found.png"})
    if not product.image_src:
        return jsonify({"success": False, "message": "Image not found for the specified product", "url": "https://pinoss.com/kokomi/i/2023/10/20/Product_Not_Found.png"})
    return jsonify({"success": True, "message": "Image retrieved successfully", "url": product.image_src})


# Provide get image from user method for a user to get the image of a user
@image_bp.route('/get_image_user', methods=['GET'])
def get_image_from_user():
    phone = request.args.get('phone')

    # verify if the phone is provided
    if not phone:
        return jsonify({"success": False, "message": "Phone number is required", "url": "https://pinoss.com/kokomi/i/2023/10/20/default_image.jpg"})

    # find the user by phone
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return jsonify({"success": False, "message": "User not found", "url": "https://pinoss.com/kokomi/i/2023/10/20/default_image.jpg"})
    if not user.image_src:
        return jsonify({"success": False, "message": "Image not found for the specified user", "url": "https://pinoss.com/kokomi/i/2023/10/20/default_image.jpg"})
    return jsonify({"success": True, "message": "Image retrieved successfully", "url": user.image_src})






