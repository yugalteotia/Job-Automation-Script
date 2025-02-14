from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Define a fake valid token for testing (Replace this with actual logic if needed)
VALID_BEARER_TOKEN = "test_mock_token"

@app.route('/api/pmsStayRaw/unsetEmptyOrNullFields', methods=['PUT'])
def mock_server():
    # Check Authorization Header
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"result": {"success": False, "message": "Missing or invalid Authorization header"}}), 401
    
    # Extract token from "Bearer <token>"
    token = auth_header.split("Bearer ")[1]
    
    if token != VALID_BEARER_TOKEN:
        return jsonify({"result": {"success": False, "message": "Unauthorized"}}), 403

    # Get propertyIds parameter
    property_ids = request.args.get("propertyIds")
    
    if not property_ids:
        return jsonify({"result": {"success": False, "message": "Missing propertyIds"}}), 400

    # Simulate delay before response (1 minute)
    time.sleep(60)

    return jsonify({"result": {"success": True, "message": "Jobs started successfully"}}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Runs on http://127.0.0.1:5000
