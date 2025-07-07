from flask import Flask, request
from dateutil import parser
from pymongo import MongoClient
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# mongo URL
MONGO_URI = "<your-mongo-url>"
client = MongoClient(MONGO_URI)
db = client["webhookdb"]
collection = db["events"]

@app.route("/")
def home():
    return "Webhook receiver is running!"

#actual webhook fetch
@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event_type == "push":
        author = payload["head_commit"]["author"]["name"]
        to_branch = payload["ref"].split("/")[-1]
        timestamp = payload["head_commit"]["timestamp"]
        message = payload["head_commit"]["message"]

        action = "Merge" if "merge pull request" in message.lower() else "Push"

        # store in Mongo
        event = {
            "author": author,
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": format_time(timestamp),
            "action": action
        }
        collection.insert_one(event)
        print(f"Stored {action} event: {event}")

    elif event_type == "pull_request":
        author = payload["pull_request"]["user"]["login"]
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]
        timestamp = payload["pull_request"]["created_at"]

        # again store in Mongo
        event = {
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": format_time(timestamp),
            "action": "Pull"
        }
        collection.insert_one(event)
        print(f"Stored Pull event: {event}")

    else:
        print(f"Unhandled event type: {event_type}")

    return "", 200

def format_time(timestamp):
    dt = parser.isoparse(timestamp)
    return dt.strftime("%#d %B %Y - %#I:%M %p UTC")


@app.route("/events", methods=["GET"])
def get_events():
    # shows all the events sort(newest first)
    docs = collection.find().sort("timestamp", -1)
    result = []

    for doc in docs:
        result.append({
            "author": doc.get("author"),
            "from_branch": doc.get("from_branch"),
            "to_branch": doc.get("to_branch"),
            "timestamp": doc.get("timestamp"),
            "action": doc.get("action")
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
