from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/hr-agent", methods=["POST"])
def hr_agent():
    try:
        data = request.get_json(force=True)
        user_query = data.get("query")

        if not user_query:
            return jsonify({"error": "Missing 'query' in request"}), 400

        # Simulated logic for demonstration
        if "leave" in user_query.lower():
            answer = (
                "You are entitled to a minimum of 14 days of annual leave per year "
                "as per the company's leave policy. Leave must be applied for in advance "
                "and approved by your supervisor."
            )
        else:
            answer = "I'm not sure how to answer that. Please contact HR for more details."

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
