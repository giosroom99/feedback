import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from bson.binary import Binary
import uuid

import datetime
import db
import feedback_predicter as fp

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/user', methods=['GET'])
@cross_origin()
def get_users():
    return db.get_users(), 200

@app.route('/user/<user_id>', methods=['GET'])
@cross_origin()
def get_user(user_id):
    return db.get_user(user_id), 200

@app.route('/user/<user_id>/chat', methods=['GET'])
@cross_origin()
def get_chats(user_id):
    return db.get_chats(user_id), 200

@app.route('/chat', methods=['POST'])
@cross_origin()
def upload_newmessage():
    data = request.get_json()

    sender_ID = data.get("sender_ID")
    recipient_ID = data.get("recipient_ID")
    message_text = data.get("message_text")
    is_manager_response = data.get("is_manager_response") == True
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
    sentiment = "N/A"

    if not is_manager_response:
        sentiment = fp.predict_sentiment(message_text)

    message = {
        "chat_ID": str(uuid.uuid4()),
        "sender_ID": sender_ID,
        "recipient_ID": recipient_ID,
        "message_text": message_text,
        "timestamp": timestamp,
        "is_manager_response": is_manager_response,
        "is_read": False,
        "sentiment": sentiment
    }

    print("Posting message")
    db.post_message(message)
    return "Success", 201

@app.route('/login', methods=['POST'])
@cross_origin()
def attempt_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    res = db.attempt_login(email, password)
    print(res)
    if res == "":
        return jsonify({"error": "Login attempt failed"}), 401
    else:
        return jsonify({"data": res}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)


