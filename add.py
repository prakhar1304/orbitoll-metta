from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
from hyperon import MeTTa

app = Flask(__name__)

# Path to your metta file
METTA_FILE = "my_knowledge.metta"
TRANSACTION_FILE = "transactionhistory.metta"

# Enable CORS for the entire app
CORS(app)



metta = MeTTa()
vehicle_metta = MeTTa()
location_metta = MeTTa()

with open(METTA_FILE, "r") as f:
    metta.run(f.read())


# Util to format and append to METTA file
def save_vehicle_to_metta(veh_no, full_name, wallet, veh_type, rc_detail):
    # Format the data as METTA-style line
    line_to_insert = f"({veh_no} ({full_name}) {wallet} {veh_type} {rc_detail})\n"
    insert_before_line = '(= (vehicalDetail $n)'

    with open(METTA_FILE, "r") as f:
        lines = f.readlines()

    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        if insert_before_line in line and not inserted:
            # Insert the new data just before this line
            new_lines.append(line_to_insert)
            inserted = True
        new_lines.append(line)

    if not inserted:
        # If the target line isn't found, just append at the end
        new_lines.append("\n" + line_to_insert)

    with open(METTA_FILE, "w") as f:
        f.writelines(new_lines)

    return line_to_insert.strip()

#
def save_transaction_to_metta(veh_no, time, date, name, price):
    # Format the transaction data in the expected MeTTa format
    line = f"({veh_no} \"{time}\" \"{date}\" ({name}) {price})\n"
    
    # Append to the transaction file
    with open(TRANSACTION_FILE, "a") as f:
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
        

        # query = f"!(vehicalDetail {vehicle_number})"
        # result = metta.run(query)

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


@app.route("/get-vehicle", methods=["GET"])
def get_vehicle_by_number():
    try:
        vehicle_number = request.args.get("vehicle_number")

        if not vehicle_number:
            return jsonify({"error": "Missing 'vehicle_number' parameter"}), 400

        query = f"!(vehicalDetail {vehicle_number})"
        result = metta.run(query)
        output = print(result)

        if not result or not result[0]:
            return jsonify({"message": f"No data found for vehicle number '{vehicle_number}'"}), 404

        # Convert result to readable JSON
        # E.g., ["vehical_no", "CG07AU599", "owner name", "PRAKHAR MADHARIA", "wallet address", "0xABC123DEF456", ...]
        # Grab the actual tuple
        raw_data = result[0][0]  # ← list of 1 tuple → extract the tuple
        print(raw_data)
         # Convert to list
        data = raw_data.get_children()
        print(data)

        vehicle_data = {}
        for i in range(0, len(data) - 1, 2):  # Safe pairing
            key = str(data[i]).strip(":").replace(" ", "_").replace('"', '')
            value = str(data[i + 1]).replace('"', '')
            vehicle_data[key] = value

        return jsonify({"vehicle": vehicle_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/log-transaction", methods=["POST"])
def log_transaction():
    try:
        data = request.get_json()

        veh_no = data.get("vehicle_number")
        time = data.get("time")
        date = data.get("date")
        name = data.get("name")
        price = data.get("price")

        # Basic validation
        if not all([veh_no, time, date, name, price]):
            return jsonify({"error": "All fields are required!"}), 400

        # Save transaction to .metta file
        fact = save_transaction_to_metta(veh_no, time, date, name, price)

        return jsonify({
            "message": "✅ Transaction logged successfully!",
            "transaction_fact": fact
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


LOCATION_FILE = "helloworld.metta"

# Load MeTTa engine
metta = MeTTa()
with open(LOCATION_FILE, "r") as f:
    location_metta.run(f.read())


@app.route("/location-details", methods=["GET"])
def get_location_details():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Missing 'place' query parameter!"}), 400

    try:
        query = f"!(isdetail {place})"
        result = location_metta.run(query)
        print(f"MeTTa result: {result}")

        if not result or not result[0]:
            return jsonify({"message": f"No details found for '{place}'."}), 404

        # Get all children from the result
        data = result[0][0].get_children()
        
        # Initialize the response structure
        response = {
            "place": place,
            "detail": {
                "travelcost": {}
            }
        }

        # Parse the data based on specific keys
        i = 0
        while i < len(data):
            current = str(data[i]).replace('"', '')
            
            # Handle no of days
            if current == "no of days" and i+1 < len(data):
                response["detail"]["total days"] = int(str(data[i+1]))
                i += 2
            
            # Handle food cost
            elif "food cost" in current and i+1 < len(data):
                response["detail"]["food price per day"] = int(str(data[i+1]))
                i += 2
            
            # Handle hotel cost
            elif "hotel cost" in current and i+1 < len(data):
                response["detail"]["hotelprice perday"] = int(str(data[i+1]))
                i += 2
            
            # Handle transportation
            elif "bike car bus" in current and i+3 < len(data):
                response["detail"]["travelcost"]["bike"] = int(str(data[i+1]))
                response["detail"]["travelcost"]["car"] = int(str(data[i+2]))
                response["detail"]["travelcost"]["bus"] = int(str(data[i+3]))
                i += 4
            
            # Handle best time
            elif "best time" in current and i+1 < len(data):
                response["detail"]["best time to visit"] = str(data[i+1])
                i += 2
            
            # Skip the place name at the beginning
            elif current == place:
                i += 1
            
            # Handle any other data
            else:
                i += 1

        return jsonify(response), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500







@app.route('/location-coords')
def location_coords():
    place = request.args.get('place')
    if not place:
        return jsonify({"error": "Missing 'place' query parameter!"}), 400

    query = f"!(isloglat {place})"
    result = location_metta.run(query)
    print(result)

    checkpoints = []

      # Check if we got a valid result
    if result and isinstance(result[0], list):
        # Process each tourist place in the result
        for idx, atom in enumerate(result[0], 1):
            print(f"\nAtom #{idx}: {atom}")
            print("Type:", type(atom))
            
            # Get the atom's children/parts
            parts = atom.get_children()
            
            if len(parts) >= 4:  # Make sure we have enough parts
                # parts should be ["touristplace", name, "has logitue latitue", coords]
                name = str(parts[1])
                
                # Get coords which is the 4th element (index 3)
                coords = parts[3].get_children()
                
                if len(coords) >= 2:
                    # Convert coordinates to float
                    latitude  = float(str(coords[0]))
                    longitude = float(str(coords[1]))

                    checkpoints.append({
                        "checkpoint": idx,
                        "name": name,
                        "longitude": longitude,
                        "latitude": latitude
                    })

    return jsonify({
        "destination": place,
        "checkpoints": checkpoints
    })


    
if __name__ == "__main__":
    app.run(debug=True)
