from flask import jsonify
from app.management.config import database


def view_latest_image():
    image = database.image_collection.find_one(sort=[("timestamp", -1)])
    if not image:
        return jsonify({"error": "No image found"}), 404

    return jsonify({
        "timestamp": image["timestamp"],
        "detections": image["detected_objects"],
        "image_raw_base64": image["image_raw_base64"],
        "image_annotated_base64": image["image_annotated_base64"]
    }), 200
