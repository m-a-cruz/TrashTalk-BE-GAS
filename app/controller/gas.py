from flask import jsonify,Response, request
from bson import json_util
from app.management.config import database
import datetime
from extensions import socketio

def record_gas_level():
    data = request.json
    record = {"timestamp": datetime.datetime.now(),"data": data, }
    database.gas_collection.insert_one(record)
    
    if data["type"] == "Safe": store_notif("Safe", "Gas levels are safe.")
    elif data["type"] == "Warning": store_notif("Warning", "Warning: Gas levels rising. Take precautions!")
    elif data["type"] == "Critical": store_notif("Critical", "Critical: High gas levels! Urgent action required!")
    elif data["type"] == "Explosive": store_notif("Explosive", "Explosive: Explosive gas levels! Immediate evacuation!")
            
    return jsonify({"message": "Gas data recorded successfully"}), 201

def fetch_gas_chart():
    gas_chart = list(database.chart_collection.find())
    response = Response(json_util.dumps(gas_chart), mimetype='application/json')
    return response, 200

def store_notif(type,message):
    notification = {
        "timestamp": datetime.datetime.utcnow(),
        "data": {
            "type": type,
            "message": message,
            "status": "Active"
        }
    }
    database.notification_collection.insert_one(notification)
    socketio.emit("new_notification", json_util.dumps(notification))