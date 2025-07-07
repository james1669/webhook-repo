TechStax Webhook Assignment Submission
--------------------------------------

Submitted by: James Bright

Contents:
---------
- webhook-repo/     : Flask backend that receives GitHub webhook events and stores them in MongoDB Atlas.
- action-repo/      : Dummy GitHub repository used to generate webhook events like Push, Pull, and Merge.
- index.html        : Frontend UI (polls the backend every 15 seconds to display the latest event).
- requirements.txt  : Python dependency list for running the Flask backend.
- README.txt        : This instruction and documentation file.

How it works:
-------------
- The Flask app listens for GitHub webhook events at the `/webhook` endpoint.
- It stores push, pull, and merge events into a MongoDB Atlas cluster.
- Events are timestamped and structured with author, from_branch, to_branch, action type, and time.
- The frontend (`index.html`) polls the `/events` endpoint every 15 seconds and displays the **latest event only** in a color-coded table.
- Duplicate or previously displayed events are not reloaded, per assignment instructions.

How to run:
-----------
1. Install Python dependencies:
   pip install -r requirements.txt

2. Start the Flask server:
   python app.py

3. Expose your local Flask server using ngrok:
   ngrok http 5000

   - Copy the generated HTTPS URL from ngrok.
   - Use it in your GitHub webhook settings like:
     https://<example-ngrok-link>/webhook

4. Open `index.html` in your browser (double-click or use Live Server in VS Code).

Webhook Testing:
----------------
- GitHub webhook is configured to point to the ngrok URL (e.g. `/webhook`).
- Trigger events by:
   - Pushing new commits to `action-repo`
   - Creating Pull Requests
   - Merging PRs

Notes:
------
- Frontend uses simple polling (15-second interval) to fetch and show the latest event only.
- Backend uses CORS to support cross-origin access from `index.html`.
- Events are stored in MongoDB Atlas and served in descending order by time.
- Timestamps are displayed in the format: `7 July 2025 - 1:23 PM UTC`.
- Favicon and duplicate entries are handled cleanly.
- Merge detection via commit message ("merge pull request") is implemented for bonus credit.

TechStax Submission Compliance:
-------------------------------
✔️ Push, Pull, and Merge (bonus) webhook events supported  
✔️ No duplicate event display  
✔️ Data formats and timestamp display are clean and readable  
✔️ Code is well-indented, commented, and readable  
✔️ Frontend displays events in tabular format with action-based row highlighting  
✔️ Includes both GitHub repo links (webhook-repo and action-repo)

Thank you for reviewing my submission!
