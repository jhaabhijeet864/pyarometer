from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from compatibility import calculate_compatibility
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Connection
mongo_uri = os.environ.get("MONGODB_URI")
client = MongoClient(mongo_uri, server_api=ServerApi('1'))

try:
    # Send a ping to confirm connection
    client.admin.command('ping')
    print("✅ Connected to MongoDB!")
    db = client.love_predictor
except Exception as e:
    print("❌ MongoDB connection error:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    name1 = request.form.get('name1')
    name2 = request.form.get('name2')
    
    if not name1 or not name2:
        return render_template('index.html', error="Please enter both names")
    
    # Calculate compatibility
    compatibility = calculate_compatibility(name1, name2)
    
    # Store in MongoDB
    try:
        db.compatibility_checks.insert_one({
            'name1': name1,
            'name2': name2,
            'compatibility': compatibility,
            'created_at': datetime.utcnow()
        })
    except Exception as e:
        print(f"Database error: {e}")
        # Continue even if DB storage fails
    
    # Generate a message based on compatibility score
    message = get_compatibility_message(compatibility)
    
    return render_template('result.html', 
                           name1=name1, 
                           name2=name2, 
                           compatibility=compatibility,
                           message=message)

@app.route('/api/compatibility', methods=['POST'])
def api_compatibility():
    data = request.get_json()
    name1 = data.get('name1')
    name2 = data.get('name2')
    
    if not name1 or not name2:
        return jsonify({"error": "Please provide both names"}), 400
    
    # Calculate compatibility
    compatibility = calculate_compatibility(name1, name2)
    
    # Store in MongoDB
    try:
        db.compatibility_checks.insert_one({
            'name1': name1,
            'name2': name2,
            'compatibility': compatibility,
            'created_at': datetime.utcnow()
        })
    except Exception as e:
        print(f"Database error: {e}")
    
    return jsonify({"compatibility": compatibility})

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

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)