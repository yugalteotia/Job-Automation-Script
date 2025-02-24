from flask import Flask, request, jsonify
import time
import config

app = Flask(__name__)

VALID_BEARER_TOKEN = config.BEARER_TOKEN

# Existing endpoint for main script (PUT)
@app.route('/api/pmsStayRaw/unsetEmptyOrNullFields', methods=['PUT'])
def mock_unset_empty_fields():
    # Check Authorization Header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"result": {"success": False, "message": "Missing or invalid Authorization header"}}), 401

    token = auth_header.split("Bearer ")[1]
    if token != VALID_BEARER_TOKEN:
        return jsonify({"result": {"success": False, "message": "Unauthorized"}}), 403

    property_ids = request.args.get("propertyIds")
    if not property_ids:
        return jsonify({"result": {"success": False, "message": "Missing propertyIds"}}), 400

    # Simulate delay (1 minute) before responding
    time.sleep(60)

    return jsonify({"result": {"success": True, "message": "Jobs started successfully"}}), 200

# New endpoint for helper script (GET)
@app.route('/api/feedConfigurations', methods=['GET'])
def mock_properties():
    # Check Authorization Header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"result": []}), 401  # Unauthorized

    token = auth_header.split("Bearer ")[1]
    if token != VALID_BEARER_TOKEN:
        return jsonify({"result": []}), 403  # Forbidden

    # Sample data simulating the API response (without requiring propertyId)
    sample_data = [
        {
            "id": "5bd7e8f56348e024a8ef61c1",
            "incomingSystem": "MARS",
            "clientCode": "LOEWS",
            "propertyCode": "LCHI",
            "propertyId": "2",
            "status": "ACTIVE"
        },
        {
            "id": "5c90b86515b56b5aa882beb6",
            "incomingSystem": "MARS",
            "clientCode": "CRHGROUP",
            "propertyCode": "BRUZH",
            "propertyId": "5",
            "status": "ACTIVE"
        },
        {
            "id": "5c90b22a15b56b5aa882be9e",
            "incomingSystem": "G3RMS",
            "clientCode": "CRHGROUP",
            "propertyCode": "CPHZH",
            "propertyId": "6",
            "status": "ACTIVE"
        },
        {
            "id": "5d67c7e44db3dc8908dcab85",
            "incomingSystem": "S_AND_C",
            "clientCode": "LANGHAM",
            "propertyCode": "TLCHI",
            "propertyId": "9",
            "status": "INACTIVE"
        }
    ]

    return jsonify({"result": sample_data}), 200  # Return all properties

if __name__ == '__main__':
    app.run(port=5000, debug=True)
