"""
world_data.py - The Cartographer's Module (Agent Epsilon)

This module contains the graph representation of Milwaukee neighborhoods
and travel cost logic.
"""

MILWAUKEE_MAP = {
    "Downtown": {
        "description": "Skyscrapers, sadness, and wind tunnels. The heart of the beast.",
        "danger_level": 3,
        "neighbors": ["East Side", "Riverwest", "Walker's Point", "Third Ward", "Near West Side"],
        "landmark": "Central Library"
    },
    "Third Ward": {
        "description": "Expensive condos and boutiques you are too poor to enter.",
        "danger_level": 1,
        "neighbors": ["Downtown", "Walker's Point"],
        "landmark": "Milwaukee Public Market"
    },
    "Riverwest": {
        "description": "Alleys, art, anarchy. Everyone looks like they play bass.",
        "danger_level": 2,
        "neighbors": ["East Side", "Downtown", "Bronzeville"],
        "landmark": "Falcon Bowl"
    },
    "Polonia": {
        "description": "The Basilica looms. Smells like incense, old bricks, and pierogis.",
        "danger_level": 2,
        "neighbors": ["Walker's Point", "Bay View"],
        "landmark": "Basilica of St. Josaphat"
    },
    "Walker's Point": {
        "description": "Industrial chic. Smells like chocolate or sewage.",
        "danger_level": 2,
        "neighbors": ["Downtown", "Bay View", "Third Ward", "Polonia"],
        "landmark": "Sobelman's"
    },
    "Bay View": {
        "description": "Hipster parents pushing $800 strollers to buy $9 donuts.",
        "danger_level": 1,
        "neighbors": ["Walker's Point", "Polonia"],
        "landmark": "The Vanguard"
    },
    "East Side": {
        "description": "Impossible parking. UWM students. The scent of Lake Michigan.",
        "danger_level": 2,
        "neighbors": ["Downtown", "Riverwest"],
        "landmark": "Wolski's"
    },
    "Near West Side": {
        "description": "Marquette University and the highway. Loud.",
        "danger_level": 3,
        "neighbors": ["Downtown", "Speed Queen Area", "Bronzeville"],
        "landmark": "Real Chili"
    },
    "Speed Queen Area": {
        "description": "The air here smells like smoked meat. It is holy ground.",
        "danger_level": 1,
        "neighbors": ["Near West Side", "Sherman Park", "Bronzeville"],
        "landmark": "Speed Queen BBQ"
    },
    "Sherman Park": {
        "description": "Historic boulevards and the best neighbors.",
        "danger_level": 2,
        "neighbors": ["Speed Queen Area", "Wauwatosa"],
        "landmark": "Sherman Phoenix"
    },
    "West Allis": {
         "description": "The Holy Land. Questionable lawn ornaments and honest people.",
         "danger_level": 1,
         "neighbors": ["Wauwatosa", "Hales Corners"],
         "landmark": "West Allis Cheese Shoppe"
    },
    "Wauwatosa": {
        "description": "The suburbs. It's quiet. Too quiet.",
        "danger_level": 1,
        "neighbors": ["Sherman Park", "West Allis"],
        "landmark": "Gilles Frozen Custard"
    },
    "Hales Corners": {
        "description": "Southwest side. Neon lights glow in the distance.",
        "danger_level": 1,
        "neighbors": ["West Allis"],
        "landmark": "Leon's Frozen Custard"
    },
    "Bronzeville": {
        "description": "Culture, business, and history.",
        "danger_level": 2,
        "neighbors": ["Riverwest", "Near West Side", "Speed Queen Area"],
        "landmark": "Gee's Clippers"
    },
    "The Center": {
        "description": "The Coggs Center. The fluorescent lights hum with malice.",
        "danger_level": 5,
        "neighbors": ["Downtown"],
        "landmark": "Economic Support Window"
    }
}

class TravelCost:
    MODES = {
        "Bus": {
            "cost": 2.25,
            "description": "High Stress Variance. It might be late. It might never come.",
            "stress_min": 0,
            "stress_max": 20
        },
        "Uber": {
            "cost": 15.00,  # High Cost
            "description": "Low Stress. You pay for the silence.",
            "stress_min": 0,
            "stress_max": 5
        },
        "Hooptie": {
            "cost": 0.00,
            "description": "Free, but 10% Breakdown Risk.",
            "breakdown_chance": 0.10,
            "stress_min": 5,
            "stress_max": 10
        },
        "Walking": {
            "cost": 0.00,
            "description": "Free, Slow. You see things you can't unsee.",
            "stress_min": 5,
            "stress_max": 15,
            "time_penalty": True
        }
    }
