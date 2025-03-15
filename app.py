from flask import Flask
from flask_cors import CORS

from flask_login import LoginManager
from config import Config
from users import auth_bp
from images import image_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all origins



# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(image_bp, url_prefix='/images')

@app.route('/')
def home():
    return "Welcome to the Image Management API! Use /auth for authentication endpoints and /images for image management."

if __name__ == '__main__':
    app.run(debug=True)
