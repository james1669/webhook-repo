from flask import Flask, request, jsonify
from dateutil import parser
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MONGO_URI = "<your-mobgo-url>"
client = MongoClient(MONGO_URI)
db = client["webhookdb"]
collection = db["events"]

@app.route("/")
def home():
    return "Webhook receiver is running!"

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
def get_all_events_sorted():
    all_docs = list(collection.find())
    if not all_docs:
        return jsonify([])

    # Parse the formatted string timestamp back to datetime
    def parse_doc(doc):
        try:
            dt = parser.parse(doc["timestamp"].replace(" UTC", ""))
            return (dt, doc)
        except:
            return (None, doc)

    parsed_docs = [parse_doc(doc) for doc in all_docs if "timestamp" in doc]
    parsed_docs = [p for p in parsed_docs if p[0] is not None]

    # Sort by parsed datetime descending
    parsed_docs.sort(key=lambda x: x[0], reverse=True)

    # Return the full sorted list
    result = []
    for _, doc in parsed_docs:
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
