import json
from flask import request, jsonify
from app.management.config import database, cipher
import jwt

def get_user():
    token = request.cookies.get("access_token_cookie")
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    try:
        payload = jwt.decode(token, cipher.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["sub"]
        user = database.users_collection.find_one({"email": user_id})
        return jsonify({"user": user}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

def update_user():
    token = request.cookies.get("access_token_cookie")
    data = request.json
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    try:
        payload = jwt.decode(token, cipher.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["sub"]
        user = database.users_collection.find_one({"email": user_id})
        if not user:
            return jsonify({"error": "User does not exist"}), 404
        
        update_data = {key: value for key, value in data.items() if key != "email"}
        database.users_collection.update_one({"email": user_id}, {"$set": update_data})
        return jsonify({"message": "User updated successfully"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

def delete_user():
    data = request.json
    user = database.users_collection.find_one({"email": data["email"]})
    if not user: return jsonify({"error": "User does not exists"}), 400

    # Delete user
    database.users_collection.delete_one({"email": data["email"]})

    return jsonify({"message": "User deleted successfully"}), 200