from flask import Flask, request, jsonify

app = Flask(__name__)

METTA_FILE = "helloworld.metta"

def parse_metta_file():
    with open(METTA_FILE, "r") as file:
        lines = file.readlines()

    facts = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith(";"):
            facts.append(line)
    return facts


def get_tourist_places_with_coords(place_name):
    facts = parse_metta_file()
    tourist_places = []

    # Step 1: find all ($spot isTouristPlace $place_name)
    for fact in facts:
        if fact.startswith(f"(") and " isTouristPlace " in fact:
            parts = fact.strip("()").split()
            if len(parts) == 3 and parts[2] == place_name:
                spot = parts[0]

                # Step 2: find corresponding ($spot hasLogLat (lat lon))
                for f in facts:
                    if f.startswith(f"({spot} hasLogLat "):
                        inner = f.strip("()").split("hasLogLat")[1].strip()
                        latlon = inner.strip("()").split()
                        if len(latlon) == 2:
                            lat, lon = latlon
                            tourist_places.append({
                                "name": spot,
                                "latitude": float(lat),
                                "longitude": float(lon)
                            })
                        break
    return tourist_places


@app.route("/location", methods=["GET"])
def get_location_info():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Missing 'place' query parameter!"}), 400

    try:
        results = get_tourist_places_with_coords(place)
        if not results:
            return jsonify({"message": f"No tourist places found for '{place}'."}), 404
        return jsonify({
            "place": place,
            "tourist_spots": results
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
