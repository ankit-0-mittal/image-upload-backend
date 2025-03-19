from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS  # ✅ Import CORS
import firebase_admin
from firebase_admin import credentials, firestore, storage
from users import auth_bp, db, login_manager  # Import from users.py

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # ✅ Allows requests from frontend (React)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:*1Local@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize database and login manager
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# 🔥 Initialize Firebase BEFORE importing `images.py`
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "image-uploader-51f18.firebasestorage.app"  # Replace with your actual Firebase Storage bucket
})

# Now import images AFTER Firebase is initialized
from images import image_bp  # ✅ This will now work

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(image_bp, url_prefix='/images')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensures the database tables are created
    app.run(debug=True)
