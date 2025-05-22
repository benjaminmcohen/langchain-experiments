import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request, abort
from functions import draft_email
import logging, os
from functools import wraps
import time
import sys

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/", methods=["GET"])
def index():
    return "✅ Flask app is running on Azure"

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    logging.info(f"Incoming Slack event: {data}")
    if data and data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8000)