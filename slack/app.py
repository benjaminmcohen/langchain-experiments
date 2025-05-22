import os
import sys
import time
import logging
from functools import wraps
from flask import Flask, request, abort, jsonify  # ✅ include jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv, find_dotenv
from functions import draft_email  # ✅ assuming this exists and is valid

# Load environment variables
load_dotenv(find_dotenv())

# Set up Slack app with bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Set up Flask app and Slack handler
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Optional: Log all incoming requests (very helpful for debugging)
@flask_app.before_request
def log_request_info():
    logging.info(f"Headers: {request.headers}")
    logging.info(f"Body: {request.get_data()}")

# Health check route
@flask_app.route("/", methods=["GET"])
def index():
    return "✅ Flask app is running on Azure"

# Slack events route
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    logging.info(f"Incoming Slack event: {data}")
    
    # Handle Slack URL verification challenge
    if data and data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})
    
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8000)
