import json
from flask import request, jsonify
from app.management.config import database, cipher
import app.management.encryption as encrypt
import jwt
from bson import json_util

def get_user():
    token = request.cookies.get("access_token_cookie")
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    try:
        payload = jwt.decode(token, cipher.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["sub"]
        user = database.users_collection.find_one({"email": user_id})
        return json_util.dumps(user), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

def update_user():
    # token = request.cookies.get("access_token_cookie")
    # if not token:
    #     return jsonify({"error": "Token is missing"}), 401
    
    data = request.json
    try:
        # payload = jwt.decode(token, cipher.SECRET_KEY, algorithms=["HS256"])
        # user_id = payload["sub"]
        user = database.users_collection.find_one({"email": data["email"]})
        if "currentPassword" in data and "password" in data:
            if not user or not encrypt.check_password(user["password"], data["currentPassword"]): 
                return jsonify({"error": "Invalid credentials"}), 401
            
            database.users_collection.update_one({"email": data["email"]}, {"$set": {"password": encrypt.hash_password(data["password"])}})
            return jsonify({"message": "Password updated successfully"}), 200

        database.users_collection.update_one({"email": data["email"]}, {"$set": {"name": data["name"]}})
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