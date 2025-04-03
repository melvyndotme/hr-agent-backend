from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Enable logging
logging.basicConfig(level=logging.INFO)

@app.route("/hr-agent", methods=["POST"])
def hr_agent():
    try:
        data = request.get_json(force=True)
        user_query = data.get("query")

        app.logger.info(f"Received query: {user_query}")

        if not user_query:
            return jsonify({"response": "Sorry, your message was empty. Could you try again?"}), 200

        # Simulated logic
        if "leave" in user_query.lower():
            answer = (
                "You are entitled to a minimum of 14 days of annual leave per year "
                "as per the company's leave policy. Leave must be applied for in advance "
                "and approved by your supervisor."
            )
        else:
            answer = (
                "I'm not sure how to answer that. Please contact HR for more details."
            )

        return jsonify({"response": answer}), 200

    except Exception as e:
        app.logger.error(f"Error handling request: {e}")
        return jsonify({"response": "Oops, something went wrong on our end. Please try again later."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
