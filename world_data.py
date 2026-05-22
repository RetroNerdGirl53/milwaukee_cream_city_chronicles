"""
world_data.py - The Cartographer's Module (Agent Epsilon)

Graph representation of Milwaukee neighborhoods and travel cost logic.
Expanded v3: Silver City, Brady Street, Amani, Mitchell Street, Harbor District, etc.
"""

MILWAUKEE_MAP = {
    "Downtown": {
        "description": "Skyscrapers, sadness, and wind tunnels. The heart of the beast. Someone is always filming a TikTok on Wisconsin Ave.",
        "danger_level": 3,
        "neighbors": ["East Side", "Riverwest", "Walker's Point", "Third Ward", "Near West Side", "Harbor District", "The Center"],
        "landmark": ["Central Library", "Safe House"]
    },
    "Third Ward": {
        "description": "Expensive condos and boutiques you are too poor to enter. A bridezilla argues about charcuterie.",
        "danger_level": 1,
        "neighbors": ["Downtown", "Walker's Point", "Harbor District"],
        "landmark": "Milwaukee Public Market"
    },
    "Harbor District": {
        "description": "Water, cranes, and a brewery that smells like hope. Yachts you will never board.",
        "danger_level": 2,
        "neighbors": ["Downtown", "Third Ward", "Walker's Point"],
        "landmark": "Harbor House"
    },
    "Riverwest": {
        "description": "Alleys, art, anarchy. Everyone looks like they play bass. Someone is definitely fermenting something illegal-adjacent.",
        "danger_level": 2,
        "neighbors": ["East Side", "Downtown", "Bronzeville", "Brady Street", "Harambee"],
        "landmark": "Falcon Bowl"
    },
    "Brady Street": {
        "description": "Italian flags, patio season, and a guy who says he knew you in high school (he didn't).",
        "danger_level": 2,
        "neighbors": ["East Side", "Riverwest"],
        "landmark": ["Art Bar", "Glory Days"]
    },
    "Polonia": {
        "description": "The Basilica looms. Smells like incense, old bricks, and pierogis — with a side of reality.",
        "danger_level": 7,
        "neighbors": ["Walker's Point", "Bay View", "Mitchell Street", "Lincoln Village"],
        "landmark": ["Basilica of St. Josaphat", "Stop-N-Rob"],
    },
    "Lincoln Village": {
        "description": "Polish Village south. Kielbasa in the air. Your babcia would approve of your parking spot (barely).",
        "danger_level": 3,
        "neighbors": ["Polonia", "Mitchell Street"],
        "landmark": "Polish Center of Wisconsin"
    },
    "Mitchell Street": {
        "description": "The corridor. Thrift stores, elote carts, and opinions about everything.",
        "danger_level": 4,
        "neighbors": ["Polonia", "Silver City", "Walker's Point", "Lincoln Village"],
        "landmark": "El Trucko"
    },
    "Silver City": {
        "description": "6th and Oklahoma energy. Murals, community, and the best food you can't spell yet.",
        "danger_level": 3,
        "neighbors": ["Mitchell Street", "Walker's Point", "Near West Side"],
        "landmark": "Conejito's Place"
    },
    "Walker's Point": {
        "description": "Industrial chic. Smells like chocolate or sewage. Sometimes both.",
        "danger_level": 2,
        "neighbors": ["Downtown", "Bay View", "Third Ward", "Polonia", "Mitchell Street", "Silver City", "Harbor District"],
        "landmark": "Sobelman's"
    },
    "Bay View": {
        "description": "Hipster parents pushing $800 strollers to buy $9 donuts. Someone is podcasting about it.",
        "danger_level": 1,
        "neighbors": ["Walker's Point", "Polonia"],
        "landmark": "The Vanguard"
    },
    "East Side": {
        "description": "Impossible parking. UWM students. Lake Michigan—and the abandoned boat everyone visits like it's Summerfest.",
        "danger_level": 2,
        "neighbors": ["Downtown", "Riverwest", "Brady Street"],
        "landmark": ["Wolski's", "Deep Thought"],
    },
    "Near West Side": {
        "description": "Marquette, Wisconsin Ave, The Rave/Eagles Club. Bucks energy by day; haunted pool and all-ages shows by night.",
        "danger_level": 3,
        "neighbors": ["Downtown", "Speed Queen Area", "Bronzeville", "Silver City", "Amani", "The Center"],
        "landmark": ["Real Chili", "Deer District", "The Rave"],
    },
    "Amani": {
        "description": "Community gardens, block clubs, and people who actually know their neighbors' names.",
        "danger_level": 4,
        "neighbors": ["Near West Side", "Sherman Park", "Bronzeville", "Washington Heights"],
        "landmark": "Coffee Makes You Black"
    },
    "Washington Heights": {
        "description": "Tree-lined streets and homeowners who email the alderperson in ALL CAPS.",
        "danger_level": 2,
        "neighbors": ["Amani", "Sherman Park", "Speed Queen Area"],
        "landmark": "Washington Park"
    },
    "Speed Queen Area": {
        "description": "The air here smells like smoked meat. It is holy ground. Do not rush a pitmaster.",
        "danger_level": 1,
        "neighbors": ["Near West Side", "Sherman Park", "Bronzeville", "Washington Heights"],
        "landmark": "Speed Queen BBQ"
    },
    "Sherman Park": {
        "description": "Historic boulevards and the best neighbors. Mrs. Higgins has eyes on this block.",
        "danger_level": 2,
        "neighbors": ["Speed Queen Area", "Wauwatosa", "Amani", "Washington Heights"],
        "landmark": "Sherman Phoenix"
    },
    "Harambee": {
        "description": "King Drive history. Murals that make you sit in your car a little longer.",
        "danger_level": 3,
        "neighbors": ["Riverwest", "Bronzeville"],
        "landmark": "America's Black Holocaust Museum"
    },
    "West Allis": {
        "description": "The Holy Land. Questionable lawn ornaments and honest people who say what they mean.",
        "danger_level": 1,
        "neighbors": ["Wauwatosa", "Hales Corners"],
        "landmark": "West Allis Cheese Shoppe"
    },
    "Wauwatosa": {
        "description": "The suburbs. It's quiet. Too quiet. Someone called the cops on a lemonade stand.",
        "danger_level": 1,
        "neighbors": ["Sherman Park", "West Allis"],
        "landmark": "Gilles Frozen Custard"
    },
    "Hales Corners": {
        "description": "Southwest side. Neon lights glow in the distance. Leon's is a pilgrimage.",
        "danger_level": 1,
        "neighbors": ["West Allis"],
        "landmark": "Leon's Frozen Custard"
    },
    "Bronzeville": {
        "description": "Culture, business, and history. Gee's Clippers still has the best conversation in the city.",
        "danger_level": 2,
        "neighbors": ["Riverwest", "Near West Side", "Speed Queen Area", "Harambee", "Amani"],
        "landmark": "Gee's Clippers"
    },
    "The Center": {
        "description": "The Coggs Center. The fluorescent lights hum with malice. Your timesheet is judging you.",
        "danger_level": 5,
        "neighbors": ["Downtown", "Near West Side"],
        "landmark": "Economic Support Window"
    }
}

# Neighborhoods where gentrification meter hits hardest
GENTRIFIED_NEIGHBORHOODS = {"Third Ward", "Bay View", "Harbor District", "Brady Street", "Downtown"}

class TravelCost:
    MODES = {
        "Bus": {
            "cost": 2.25,
            "description": "MCTS: High stress variance. It might be late. It might never come. Someone is playing music without headphones.",
            "stress_min": 0,
            "stress_max": 20
        },
        "Uber": {
            "cost": 15.00,
            "description": "Low stress. You pay for the silence and a driver who says 'rough neighborhood' about YOUR neighborhood.",
            "stress_min": 0,
            "stress_max": 5
        },
        "Hooptie": {
            "cost": 0.00,
            "description": "Free, but 10% breakdown risk. Check engine light has been on since 2019.",
            "breakdown_chance": 0.10,
            "stress_min": 5,
            "stress_max": 10
        },
        "Streetcar": {
            "cost": 1.00,
            "description": "Hop: Only useful if Downtown-adjacent. Tourists wave at you.",
            "stress_min": 2,
            "stress_max": 8,
            "downtown_only": True,
        },
        "Bublr": {
            "cost": 3.00,
            "description": "Bike share. Lakefront wind. Thigh burn. One wheel always wobbles.",
            "stress_min": 3,
            "stress_max": 12,
        },
        "Walking": {
            "cost": 0.00,
            "description": "Free, slow. You see things you can't unsee. Seasonal suffering included.",
            "stress_min": 5,
            "stress_max": 15,
            "time_penalty": True
        }
    }
