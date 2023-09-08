from flask import Flask, jsonify, request
from database import db
from .model.user_model import User # Import the User model from models.py
from app.controller.user_controller import user_blueprint  # Import the user_blueprint

app = Flask(__name__)

# Replace 'your_database_uri' with your PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@192.168.226.246/db_mediaService'

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Check the database connection status
@app.route('/api/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        # Perform a simple database query to check the connection
        query = db.text('SELECT 1')
        db.session.execute(query)
        return jsonify({'message': 'Database connection successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)}), 500


# Register the user_blueprint
app.register_blueprint(user_blueprint)
