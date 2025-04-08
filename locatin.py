from flask import Flask, request, jsonify
from hyperon import MeTTa
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
METTA_FILE = "helloworld.metta"

# Load MeTTa engine
metta = MeTTa()
with open(METTA_FILE, "r") as f:
    metta.run(f.read())



@app.route('/location-coords')
def location_coords():
    place = request.args.get('place')
    if not place:
        return jsonify({"error": "Missing 'place' query parameter!"}), 400

    query = f"!(isloglat {place})"
    result = metta.run(query)
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



@app.route("/location-details", methods=["GET"])
def get_location_details():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Missing 'place' query parameter!"}), 400

    try:
        query = f"!(isdetail {place})"
        result = metta.run(query)
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


if __name__ == "__main__":
    app.run(debug=True)
