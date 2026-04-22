import os
from flask import Flask, jsonify, request
import mysql.connector

# Initialize the Flask application
app = Flask(__name__)

# Tells Flask NOT to sort your JSON keys alphabetically
app.json.sort_keys = False  

# Set the JWT Secret Key directly from the Docker environment
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# Database configuration dictionary (populated by docker-compose .env)
db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'database': os.environ.get('DB_NAME')
}

def get_db_connection():
    """
    Creates and returns a connection to the MySQL database.
    """
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['GET'])
def health_check():
    """
    A simple health check to verify the API is running and can talk to the DB.
    """
    try:
        # Try to open and immediately close a connection to test it
        conn = get_db_connection()
        conn.close()
        db_status = "Connected to MySQL successfully!"
    except Exception as e:
        db_status = f"Failed to connect to MySQL: {str(e)}"

    return jsonify({
        "status": "success",
        "api_message": "API Skeleton is up and running via Gunicorn!",
        "database_status": db_status
    }), 200