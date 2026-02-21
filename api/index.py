from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_info():
    number = request.args.get('num')
    if not number:
        return jsonify({"error": "Number missing. Use ?num=+91xxx"}), 400

    try:
        # Default region "IN" add kiya hai error fix karne ke liye
        parsed_number = phonenumbers.parse(number, "IN") 
        
        if not phonenumbers.is_valid_number(parsed_number):
            return jsonify({"status": "error", "message": "Invalid number"}), 400

        data = {
            "status": "success",
            "country": geocoder.description_for_number(parsed_number, "en"),
            "operator": carrier.name_for_number(parsed_number, "en"),
            "timezone": list(timezone.time_zones_for_number(parsed_number)),
            "international": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        }
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "API is active! Use /api?num=+91xxxxxxxxxx"

app = app

