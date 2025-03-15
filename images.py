from flask import Blueprint, request, jsonify
from firebase_admin import storage
from flask_login import login_required

# Blueprint for image management
image_bp = Blueprint('images', __name__)

@image_bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
    file = request.files['file']
    if not file:
        return jsonify({"message": "No file provided!"}), 400
    
    # Upload to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    
    return jsonify({"message": "Image uploaded successfully!"}), 201

@image_bp.route('/images', methods=['GET'])
@login_required
def list_images():
    bucket = storage.bucket()
    blobs = bucket.list_blobs()
    image_urls = [blob.public_url for blob in blobs]
    
    return jsonify({"images": image_urls}), 200
