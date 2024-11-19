from flask import jsonify
def validate_registration_data(data):
    """Validate the incoming data for user registration."""
    required_fields = ["username", "email", "password"]

    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, jsonify({"message": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Additional checks (e.g., email format, password strength) can be added here
    if len(data["password"]) < 6:
        return False, jsonify({"message": "Password must be at least 6 characters long."}), 400

    return True, None, None

def validate_login_data(data):
    """Validate the incoming data for user login."""
    required_fields = ["email", "password"]

    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, jsonify({"message": f"Missing fields: {', '.join(missing_fields)}"}), 400

    return True, None, None