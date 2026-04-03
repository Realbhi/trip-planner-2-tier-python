from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

LOCATIONS = [
    {"id": 1, "name": "Goa", "country": "India", "type": "Beach", "best_season": "November – February", "description": "Sun-kissed beaches, Portuguese-era forts, and vibrant nightlife.", "rating": 4.7},
    {"id": 2, "name": "Manali", "country": "India", "type": "Mountain", "best_season": "March – June", "description": "Snow-capped peaks, river valleys, and the famous Rohtang Pass.", "rating": 4.8},
    {"id": 3, "name": "Jaipur", "country": "India", "type": "Heritage", "best_season": "October – March", "description": "The Pink City — palaces, forts, and royal Rajasthani cuisine.", "rating": 4.6},
    {"id": 4, "name": "Kerala", "country": "India", "type": "Nature", "best_season": "September – March", "description": "Backwaters, tea gardens, and Ayurvedic retreats.", "rating": 4.9},
    {"id": 5, "name": "Leh-Ladakh", "country": "India", "type": "Adventure", "best_season": "June – September", "description": "High-altitude desert, ancient monasteries, and world-class biking.", "rating": 4.9},
]

MUST_VISIT = {
    "Goa": [
        {"place": "Baga Beach", "category": "Beach", "tip": "Visit at sunrise for a crowd-free experience."},
        {"place": "Basilica of Bom Jesus", "category": "Heritage", "tip": "A UNESCO World Heritage Site."},
        {"place": "Dudhsagar Falls", "category": "Nature", "tip": "Accessible only by jeep; best after monsoon."},
        {"place": "Anjuna Flea Market", "category": "Shopping", "tip": "Every Wednesday — haggle hard!"},
    ],
    "Manali": [
        {"place": "Rohtang Pass", "category": "Adventure", "tip": "Book permits online a day ahead."},
        {"place": "Solang Valley", "category": "Nature", "tip": "Paragliding and zorbing available in summer."},
        {"place": "Hadimba Temple", "category": "Heritage", "tip": "A 16th-century wooden temple inside a cedar forest."},
        {"place": "Old Manali", "category": "Culture", "tip": "Great cafes and the real local vibe."},
    ],
    "Jaipur": [
        {"place": "Amber Fort", "category": "Heritage", "tip": "Take the elephant ride for a royal feel."},
        {"place": "Hawa Mahal", "category": "Heritage", "tip": "Best viewed from the cafe opposite."},
        {"place": "Jal Mahal", "category": "Scenic", "tip": "Floats in Man Sagar Lake — magical at dusk."},
        {"place": "Johri Bazaar", "category": "Shopping", "tip": "Best place for authentic Rajasthani jewellery."},
    ],
    "Kerala": [
        {"place": "Alleppey Backwaters", "category": "Nature", "tip": "Overnight houseboat is the best way to experience it."},
        {"place": "Munnar Tea Gardens", "category": "Scenic", "tip": "Drive through at dawn for misty views."},
        {"place": "Periyar Wildlife Sanctuary", "category": "Wildlife", "tip": "Elephant sightings on boat safaris."},
        {"place": "Varkala Cliff Beach", "category": "Beach", "tip": "Cliffside restaurants with incredible sunset views."},
    ],
    "Leh-Ladakh": [
        {"place": "Pangong Lake", "category": "Scenic", "tip": "Camp overnight — the colour shifts are unreal."},
        {"place": "Nubra Valley", "category": "Adventure", "tip": "Double-hump Bactrian camel rides available."},
        {"place": "Thiksey Monastery", "category": "Culture", "tip": "Attend the 6 AM prayer for an authentic experience."},
        {"place": "Magnetic Hill", "category": "Quirky", "tip": "A classic optical illusion — cars appear to roll uphill."},
    ],
}

WEATHER = {
    "Goa":        {"temp_c": 30, "condition": "Sunny",        "humidity": "75%", "wind": "15 km/h"},
    "Manali":     {"temp_c": 8,  "condition": "Partly Cloudy","humidity": "60%", "wind": "20 km/h"},
    "Jaipur":     {"temp_c": 24, "condition": "Clear",        "humidity": "35%", "wind": "10 km/h"},
    "Kerala":     {"temp_c": 28, "condition": "Humid",        "humidity": "85%", "wind": "12 km/h"},
    "Leh-Ladakh": {"temp_c": 2,  "condition": "Snowy",        "humidity": "40%", "wind": "25 km/h"},
}

ITINERARIES = {
    "Goa": [
        {"day": 1, "morning": "Arrive, check in, relax at Calangute Beach", "afternoon": "Explore Fort Aguada", "evening": "Seafood dinner at a beach shack"},
        {"day": 2, "morning": "Basilica of Bom Jesus & Old Goa churches",   "afternoon": "Dudhsagar Falls trip by jeep", "evening": "Anjuna Night Market"},
        {"day": 3, "morning": "Water sports at Baga Beach", "afternoon": "Spice plantation tour", "evening": "Sunset cruise on Mandovi River"},
    ],
    "Manali": [
        {"day": 1, "morning": "Arrive, acclimatise, stroll Old Manali", "afternoon": "Hadimba Temple", "evening": "Mall Road dinner"},
        {"day": 2, "morning": "Rohtang Pass (permit required)", "afternoon": "Snow activities at Solang Valley", "evening": "Campfire at stay"},
        {"day": 3, "morning": "Naggar Castle", "afternoon": "Great Himalayan National Park trek", "evening": "River-side bonfire"},
    ],
}

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "trip-planner-backend", "version": "1.0.0"})

@app.route("/api/locations")
def locations():
    return jsonify({"success": True, "count": len(LOCATIONS), "data": LOCATIONS})

@app.route("/api/locations/<int:loc_id>")
def location_detail(loc_id):
    loc = next((l for l in LOCATIONS if l["id"] == loc_id), None)
    if not loc:
        return jsonify({"success": False, "error": "Location not found"}), 404
    return jsonify({"success": True, "data": loc})

@app.route("/api/mustvisit")
def must_visit_all():
    return jsonify({"success": True, "data": MUST_VISIT})

@app.route("/api/mustvisit/<location>")
def must_visit(location):
    key = location.title()
    places = MUST_VISIT.get(key)
    if not places:
        return jsonify({"success": False, "error": f"No data for '{location}'", "available": list(MUST_VISIT.keys())}), 404
    return jsonify({"success": True, "location": key, "count": len(places), "data": places})

@app.route("/api/weather")
def weather_all():
    return jsonify({"success": True, "data": WEATHER})

@app.route("/api/weather/<location>")
def weather(location):
    key = location.title()
    info = WEATHER.get(key)
    if not info:
        return jsonify({"success": False, "error": f"No weather data for '{location}'"}), 404
    return jsonify({"success": True, "location": key, "data": info})

@app.route("/api/itinerary")
def itinerary_all():
    return jsonify({"success": True, "available": list(ITINERARIES.keys())})

@app.route("/api/itinerary/<location>")
def itinerary(location):
    key = location.title()
    plan = ITINERARIES.get(key)
    if not plan:
        return jsonify({"success": False, "error": f"No itinerary for '{location}'", "available": list(ITINERARIES.keys())}), 404
    return jsonify({"success": True, "location": key, "days": len(plan), "data": plan})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
