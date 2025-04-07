from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os

app = Flask(__name__)

# Path to your metta file
METTA_FILE = "my_knowledge.metta"

# Enable CORS for the entire app
CORS(app)

# Util to format and append to METTA file
def save_vehicle_to_metta(veh_no, full_name, wallet, veh_type, rc_detail):
    # Format the data as METTA-style line
    line = f"({veh_no} ({full_name}) {wallet} {veh_type} {rc_detail})\n"
    
    # Append it to the file
    with open(METTA_FILE, "a") as f:
        f.write(line)

    return line.strip()


# POST /register endpoint
@app.route("/register", methods=["POST"])
def register_vehicle():
    try:
        # Get JSON input
        data = request.get_json()

        veh_no = data.get("vehicle_number")
        full_name = data.get("full_name")
        wallet = data.get("wallet_address")
        veh_type = data.get("vehicle_type")
        rc_detail = data.get("rc_detail")

        # Basic validation
        if not all([veh_no, full_name, wallet, veh_type, rc_detail]):
            return jsonify({"error": "All fields are required!"}), 400

        # Save to .metta file
        fact = save_vehicle_to_metta(veh_no, full_name, wallet, veh_type, rc_detail)

        return jsonify({
            "message": "✅ Vehicle registered!",
            "metta_fact": fact
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /get endpoint to fetch all registered vehicles
@app.route("/get", methods=["GET"])
def get_all_vehicles():
    try:
        if not os.path.exists(METTA_FILE):
            return jsonify({"vehicles": []})

        with open(METTA_FILE, "r") as f:
            lines = f.readlines()

        vehicles = []
        for line in lines:
            line = line.strip()
            if not line.startswith("(") or not line.endswith(")"):
                continue
            try:
                # Remove outer parentheses and split
                content = line[1:-1]
                parts = content.split(" ", 1)
                veh_no = parts[0]
                remaining = parts[1]

                # Now split remaining
                full_name_end = remaining.find(")")
                full_name = remaining[1:full_name_end]
                rest = remaining[full_name_end+2:].split(" ")

                wallet = rest[0]
                veh_type = rest[1]
                rc_detail = rest[2]

                vehicles.append({
                    "vehicle_number": veh_no,
                    "full_name": full_name,
                    "wallet_address": wallet,
                    "vehicle_type": veh_type,
                    "rc_detail": rc_detail
                })
            except Exception:
                continue

        return jsonify({"vehicles": vehicles}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
