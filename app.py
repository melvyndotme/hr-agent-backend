from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("HR_ASSISTANT_ID")

app = Flask(__name__)

@app.route("/hr-agent", methods=["POST"])
def handle_hr_query():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing query"}), 400

    try:
        # Step 1: Create a thread
        thread = openai.beta.threads.create()

        # Step 2: Add user message
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )

        # Step 3: Run the assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Step 4: Poll for completion
        while True:
            status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if status.status == "completed":
                break
            time.sleep(1)

        # Step 5: Get response
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        full_text = messages.data[0].content[0].text.value

        # Strip citation (everything from the first "【" onward)
        response_text = full_text.split("【")[0].strip()

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
