from flask import Flask, request, jsonify, render_template, current_app
from pymongo import MongoClient
import logging
import traceback
import os
from datetime import datetime
import json
from compatibility import calculate_compatibility
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
if os.environ.get('VERCEL_ENV'):
    # For serverless environment, don't use file logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
else:
    # For local development, include file logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)

# MongoDB connection function with error handling
def get_mongo_client():
    try:
        mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri)
        # Test the connection
        client.admin.command('ping')
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "status": "error",
            "message": "Failed to load the application. Please try again later."
        }), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        name1 = request.form.get('name1')
        name2 = request.form.get('name2')
        
        if not name1 or not name2:
            return render_template('index.html', error="Please enter both names")
        
        # Calculate compatibility
        compatibility = calculate_compatibility(name1, name2)
        
        # Store in MongoDB
        try:
            client = get_mongo_client()
            db = client.pyarometer  # Initialize the db properly
            db.compatibility_checks.insert_one({
                'name1': name1,
                'name2': name2,
                'compatibility': compatibility,
                'created_at': datetime.utcnow()
            })
            client.close()  # Close the connection
        except Exception as e:
            logger.error(f"Database error: {e}")
            # Continue even if DB storage fails
        
        # Generate a message based on compatibility score
        message = get_compatibility_message(compatibility)
        
        return render_template('result.html', 
                              name1=name1, 
                              name2=name2, 
                              compatibility=compatibility,
                              message=message)
    except Exception as e:
        logger.error(f"Error in /calculate route: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "status": "error",
            "message": "Failed to process your request. Please try again later."
        }), 500

@app.route('/api/compatibility', methods=['POST'])
def api_compatibility():
    try:
        data = request.get_json()
        name1 = data.get('name1')
        name2 = data.get('name2')
        
        if not name1 or not name2:
            return jsonify({"error": "Please provide both names"}), 400
        
        # Calculate compatibility
        compatibility = calculate_compatibility(name1, name2)
        
        # Store in MongoDB
        try:
            client = get_mongo_client()
            db = client.pyarometer
            db.compatibility_checks.insert_one({
                'name1': name1,
                'name2': name2,
                'compatibility': compatibility,
                'created_at': datetime.utcnow()
            })
            client.close()
        except Exception as e:
            logger.error(f"Database error: {e}")
        
        return jsonify({"compatibility": compatibility})
    except Exception as e:
        logger.error(f"Error in /api/compatibility route: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "status": "error",
            "message": "Failed to process your request. Please try again later."
        }), 500

def get_compatibility_message(percentage):
    if percentage >= 90:
        return "Perfect match! You were destined to be together! ✨"
    elif percentage >= 75:
        return "Great match! Your love has amazing potential! 💖"
    elif percentage >= 60:
        return "Good match! You have a strong connection! 😊"
    elif percentage >= 40:
        return "Decent match. You might need to work on your relationship. 🌱"
    elif percentage >= 20:
        return "Not a great match. But opposites sometimes attract! 🤔"
    else:
        return "Maybe just be friends? The stars aren't aligned for romance. 🌟"

# Add global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the exception
    tb = traceback.format_exc()
    logger.error(f"Unhandled exception: {str(e)}\n{tb}")
    
    # Return a user-friendly error response
    return jsonify({
        "error": "An unexpected error occurred. Our team has been notified.",
        "status": "error"
    }), 500

# Update route handlers with try/except blocks
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.form.to_dict()
        timestamp = datetime.now().isoformat()
        data['timestamp'] = timestamp
        
        logger.info(f"Received submission: {json.dumps(data, default=str)}")
        
        client = get_mongo_client()
        db = client.pyarometer
        result = db.responses.insert_one(data)
        
        logger.info(f"Successfully stored submission with ID: {result.inserted_id}")
        client.close()
        
        return jsonify({"status": "success", "message": "Data submitted successfully"})
    
    except Exception as e:
        logger.error(f"Error in /submit route: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "status": "error",
            "message": "Failed to process your submission. Please try again later."
        }), 500

@app.route('/results')
def results():
    try:
        client = get_mongo_client()
        db = client.pyarometer
        responses = list(db.responses.find({}, {'_id': 0}))
        client.close()
        
        logger.info(f"Successfully retrieved {len(responses)} responses")
        return jsonify(responses)
    
    except Exception as e:
        logger.error(f"Error in /results route: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "status": "error", 
            "message": "Failed to retrieve results. Please try again later."
        }), 500

# For local development
if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0')