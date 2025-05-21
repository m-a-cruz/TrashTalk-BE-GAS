from flask import jsonify,Response, request
from bson import json_util, ObjectId
from app.management.config import database
from extensions import socketio
import datetime
# from main import socketio

# def fetch_notif():
#     notification = list(database.notification_collection.find().sort("timestamp", -1))
#     response = Response(json_util.dumps(notification), mimetype='application/json')
#     return response, 200

def fetch_notif():
    notification = list(database.notification_collection.find().sort("timestamp", -1).limit(50))
    response = Response(json_util.dumps(notification), mimetype='application/json')
    socketio.emit("notifications", response)
    return response, 200
    # return 200

def record_notif_data():
    data = request.json
    notification = {"timestamp": datetime.datetime.utcnow(),"data": data, }
    inserted = database.notification_collection.insert_one(notification)
    notification["_id"] = str(inserted.inserted_id)
    print(notification)
    socketio.emit("new_notification", notification)
    
    return jsonify({"message": "Notification recorded successfully"}), 201

def update_notif_data():
    data = request.json
    query = {"_id": ObjectId(data["id"])}
    notification = {"$set": {"data.status": data["status"]}}
    database.notification_collection.update_one(query, notification)
    socketio.emit("updated_notification", {"id": data["id"], "status": data["status"]})

    return jsonify({"message": "Notification updated successfully"}), 201

def update_many_notif():
    data = request.json
    query = {"_id": {"$in": [ObjectId(id) for id in data["ids"]]}}
    notification = {"$set": {"data.status": data["status"]}, "$currentDate": {"lastModified": True}}
    database.notification_collection.update_many(query, notification)
    socketio.emit("updated_notification", {"ids": data["ids"], "status": data["status"]})

    return jsonify({"message": "Notification updated successfully"}), 201

def delete_notif():
    data = request.json
    query = {"_id": ObjectId(data["id"])}
    database.notification_collection.delete_one(query)
    socketio.emit("deleted_notification", {"id": data["id"]})
    
    return jsonify({"message": "Notification deleted successfully"}), 200