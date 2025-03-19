import cloudinary
import cloudinary.uploader
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin 
from users import db

# ✅ Configure Cloudinary (Replace with your credentials)
cloudinary.config(
    cloud_name="df4qtnblk",
    api_key="642551397459726",
    api_secret="ma34qrTLqMmnmwPPgtd-L5tNxe8"
)

# Blueprint for image management
image_bp = Blueprint('images', __name__)

# Image model for PostgreSQL
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(255), nullable=False)

@image_bp.route('/upload', methods=['POST'])
@cross_origin() 
def upload_image():
    file = request.files.get('file')
    if not file:
        return jsonify({"message": "No file provided!"}), 400

    # ✅ Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(file)

    # ✅ Get the Cloudinary URL
    image_url = upload_result.get("secure_url")

    # ✅ Save metadata to PostgreSQL
    new_image = Image(filename=file.filename, url=image_url)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": "Upload successful!", "url": image_url}), 201

@image_bp.route('/list', methods=['GET'])
@cross_origin() 
def list_images():
    # Retrieve image metadata from PostgreSQL
    images = Image.query.all()
    image_urls = [{'filename': img.filename, 'url': img.url} for img in images]

    return jsonify({"images": image_urls}), 200
