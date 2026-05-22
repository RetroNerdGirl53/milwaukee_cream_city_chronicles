"""
world_events.py - Rotating neighborhood events, seasons, and encounter resolution.

Milwaukee-specific: festivals, parking bans, brewery smells, and the eternal construction season.
"""

import random
import datetime
from typing import Dict, Any, Optional, List, Tuple

from engine import Item

# --- SEASONS (affects walking / explore) ---
def get_season() -> str:
    month = datetime.datetime.now().month
    if month in (12, 1, 2):
        return "Winter"
    if month in (6, 7, 8):
        return "Summer"
    if month in (9, 10):
        return "Fall"
    return "Spring"


SEASON_WALK_STRESS = {
    "Winter": (15, 30),
    "Summer": (5, 12),
    "Fall": (8, 18),
    "Spring": (6, 14),
}

# --- NEIGHBORHOOD EVENT POOL (name -> list of event dicts) ---
NEIGHBORHOOD_EVENT_POOL = {
    "Riverwest": [
        {"id": "street_fest", "name": "Riverwest Street Festival", "stress_mod": -5, "travel_discount": 0.5},
        {"id": "punk_show", "name": "Basement Show at someone's duplex", "stress_mod": -8, "hp_mod": -2},
    ],
    "Polonia": [
        {"id": "basilica_bells", "name": "Basilica Bell Practice (loud)", "stress_mod": 5},
        {"id": "pierogi_run", "name": "Church Pierogi Sale", "stress_mod": -10, "cheese_bonus": True},
    ],
    "Downtown": [
        {"id": "summerfest_parking", "name": "Summerfest Lawn Parking ($40)", "stress_mod": 15, "money_sink": 20},
        {"id": "streetcar_delay", "name": "Hop Streetcar Stuck at Red Light", "stress_mod": 8},
    ],
    "Bay View": [
        {"id": "kinnickinnic_traffic", "name": "Kinnickinnic Ave Backup", "stress_mod": 6},
        {"id": "record_store_day", "name": "Record Store Day Line", "stress_mod": 4, "trust_bonus": True},
    ],
    "Bronzeville": [
        {"id": "fish_fry_line", "name": "Community Fish Fry Line (worth it)", "stress_mod": -12, "hp_mod": 15},
        {"id": "block_party", "name": "Neighborhood Block Party", "stress_mod": -15},
    ],
    "East Side": [
        {"id": "uwm_move_in", "name": "UWM Move-In Day Chaos", "stress_mod": 12},
        {"id": "brady_street_crawl", "name": "Brady Street Bar Crawl Spillover", "stress_mod": 8},
        {"id": "boat_dj_set", "name": "DJ Set at Deep Thought (beached boat)", "stress_mod": -12},
        {"id": "salvage_attempt", "name": "Another Failed Salvage of Deep Thought", "stress_mod": 8},
    ],
    "Silver City": [
        {"id": "fiesta", "name": "Silver City Fiesta", "stress_mod": -10},
        {"id": "elote_cart_war", "name": "Two Elote Carts, One Corner", "stress_mod": 3},
    ],
    "Sherman Park": [
        {"id": "phoenix_market", "name": "Sherman Phoenix Vendor Pop-Up", "stress_mod": -8},
        {"id": "pothole_protest", "name": "Pothole Protest at City Hall (caravan)", "stress_mod": -5},
    ],
    "West Allis": [
        {"id": "state_fair_energy", "name": "State Fair Energy (cream puffs in the air)", "stress_mod": -6},
        {"id": "packer_bar", "name": "Someone Yelling 'Go Pack' at 7am", "stress_mod": 2},
    ],
    "Harbor District": [
        {"id": "yacht_week", "name": "Corporate Yacht Week (ironic)", "stress_mod": 10},
        {"id": "harbor_fish", "name": "Fresh Smelt Run Smell", "stress_mod": -3},
    ],
    "Mitchell Street": [
        {"id": "thrift_haul", "name": "Mitchell Street Thrift Haul Day", "stress_mod": -7},
    ],
    "Amani": [
        {"id": "community_meeting", "name": "Community Safety Meeting", "stress_mod": -10, "reputation_bonus": 2},
    ],
    "The Center": [
        {"id": "audit_week", "name": "State Audit Week at The Center", "stress_mod": 20},
        {"id": "donut_day", "name": "Someone Brought Donuts (rare)", "stress_mod": -15},
    ],
    "Near West Side": [
        {"id": "rave_sold_out", "name": "Sold-Out Rave Show (line around Eagles Club)", "stress_mod": 6},
        {"id": "pool_chlorine", "name": "Chlorine Ghost Smell on Wisconsin Ave", "stress_mod": 8},
        {"id": "all_ages_matinee", "name": "All-Ages Matinee at The Rave", "stress_mod": -8},
        {"id": "tooth_and_nail_podcast", "name": "Band Podcast: 'Scariest Club in America'", "stress_mod": 5},
    ],
}

# Weighted random encounters with mechanical effects
ENCOUNTER_EFFECTS = {
    "Tumbleweave": {"stress": 5, "text_extra": "You consider chasing it. You do not. You are a professional."},
    "Bridge Opening": {"stress": 8, "blocks_turns": 1},
    "Found Cheese Curd": {"hp": -2, "stress": -5, "choice": "eat"},
    "Kia Boys": {"stress": 15},
    "Construction Season": {"stress": 6, "money": -5},
    "Milverine": {"stress": -20, "blessing_chance": True},
    "Festival Parking": {"money": -20, "stress": 10},
    "Winter Parking Ban": {"stress": 25, "money": -50},
    "Tom Barrett": {"stress": 3},
    "seagull": {"stress": 8, "hp": -3},
    "Ope": {"stress": -3},
    "yeast": {"stress": -2},
    "Bublr": {"stress": -5, "hp": -1},
    "County Grounds": {"stress": 5},
    "414 chant": {"stress": -8},
    "butter burger": {"hp": 10, "stress": 5},
    "snow emergency": {"stress": 20},
    "Fiserv": {"stress": -5},
    "tornado siren": {"stress": 12},
    "pickleball": {"stress": 4},
    "cannabis smell": {"stress": -4},
    "DMV line": {"stress": 15},
    "Polish Moon": {"stress": -6},
    "Deep Thought": {"stress": -12, "reputation_bonus": 1, "text_extra": "You posted a story. Three coworkers already went this week."},
    "bubbler": {"stress": -2},
    "palermos": {"stress": 3, "hp": 5},
    "county stadium": {"stress": -5},
    "mke_airport": {"stress": 5},
    "culvers": {"stress": -8, "hp": 5},
    "jj_fish": {"stress": -5, "hp": 8},
    "ians_slice": {"stress": -6, "hp": 6},
    "The Rave": {"stress": 6, "text_extra": "A roadie tells you Rob Zombie refused the basement dressing room."},
    "Grave Rave": {"stress": 8, "reputation_bonus": 1},
    "rave_pool": {"stress": 10, "hp": -3},
}

# Haunted basement pool — weighted outcomes at The Rave landmark
RAVE_POOL_HAUNTINGS = [
    {
        "id": "francis_wren",
        "weight": 3,
        "text": "A cold spot by the empty pool. Orbs of light. The name Francis Wren whispers in the chlorine.",
        "stress": 15,
        "hp": 0,
    },
    {
        "id": "ghost_jack",
        "weight": 2,
        "text": "A voice in the boiler room: 'GET OUT.' You get out. Jack (former employee?) does not apologize.",
        "stress": 20,
        "hp": -5,
    },
    {
        "id": "children_crying",
        "weight": 2,
        "text": "You hear children playing — or crying — in the basement. The pool is empty. Your caseload feels normal by comparison.",
        "stress": 18,
        "hp": 0,
    },
    {
        "id": "buddy_holly",
        "weight": 1,
        "text": "For one second you smell winter and hear a friendly guitar. Buddy Holly's ghost? He's chill. The overseer ghost is not.",
        "stress": -10,
        "hp": 5,
    },
    {
        "id": "moving_chair",
        "weight": 2,
        "text": "A chair in the boiler room moves on its own. You blink. It moves again. You leave.",
        "stress": 12,
        "hp": 0,
    },
    {
        "id": "mac_miller_wall",
        "weight": 2,
        "text": "Graffiti on the pool wall: 'I once lived now I am dead, my soul remains here…' You pay respects. Milwaukee pays respects.",
        "stress": -5,
        "hp": 0,
        "mint_token": "Pool Wall Pilgrim",
    },
    {
        "id": "all_time_low_energy",
        "weight": 1,
        "text": "Fresh Sharpie tags from a band that played IN the pool last weekend. Living legends. Haunted venue. Same thing.",
        "stress": -12,
        "hp": 0,
    },
    {
        "id": "rob_zombie",
        "weight": 1,
        "text": "Disembodied whispering in a dressing room. You understand why Rob Zombie was creeped out.",
        "stress": 14,
        "hp": 0,
    },
    {
        "id": "nothing",
        "weight": 3,
        "text": "The pool is just an empty concrete pit full of band signatures. Still spooky. Still Milwaukee.",
        "stress": -3,
        "hp": 0,
    },
]


def run_rave_pool_haunting(player, game_state) -> Dict[str, Any]:
    """
    Player descends to The Rave's haunted pool. Returns outcome dict for UI.
    """
    outcomes = RAVE_POOL_HAUNTINGS
    total = sum(o["weight"] for o in outcomes)
    roll = random.uniform(0, total)
    cumulative = 0
    chosen = outcomes[-1]
    for o in outcomes:
        cumulative += o["weight"]
        if roll <= cumulative:
            chosen = o
            break

    if chosen.get("stress"):
        if chosen["stress"] > 0:
            player.stress = min(player.max_stress, player.stress + chosen["stress"])
        else:
            player.relax(-chosen["stress"])

    if chosen.get("hp"):
        if chosen["hp"] < 0:
            player.hp = max(1, player.hp + chosen["hp"])
        else:
            player.heal(chosen["hp"])

    token_name = chosen.get("mint_token")
    minted = False
    if token_name:
        minted = True  # caller handles actual mint via registry

    game_state.reputation_414 += 1
    return {
        "text": chosen["text"],
        "id": chosen["id"],
        "mint_token": token_name if minted else None,
    }


def tick_neighborhood_events(game_state, milwaukee_map: Dict) -> Optional[str]:
    """
    Each turn, maybe start or end a neighborhood event.
    Returns flavor text if something changed.
    """
    if random.random() > 0.12:
        return None

    hood = random.choice(list(milwaukee_map.keys()))
    pool = NEIGHBORHOOD_EVENT_POOL.get(hood, [])
    if not pool:
        return None

    event = random.choice(pool)
    active = game_state.get_neighborhood_event(hood, event["id"])

    if active:
        game_state.set_neighborhood_event(hood, event["id"], False)
        return f"EVENT ENDED in {hood}: {event['name']} is over. The city exhales."
    else:
        game_state.set_neighborhood_event(hood, event["id"], True)
        return f"EVENT in {hood}: {event['name']} is happening NOW."


def get_active_event_modifiers(game_state, neighborhood: str) -> Dict[str, Any]:
    """Sum modifiers from all active events in this neighborhood."""
    mods = {"stress_mod": 0, "travel_discount": 1.0, "hp_mod": 0}
    pool = NEIGHBORHOOD_EVENT_POOL.get(neighborhood, [])
    for ev in pool:
        if game_state.get_neighborhood_event(neighborhood, ev["id"]):
            mods["stress_mod"] += ev.get("stress_mod", 0)
            if ev.get("travel_discount"):
                mods["travel_discount"] = min(mods["travel_discount"], ev["travel_discount"])
            mods["hp_mod"] += ev.get("hp_mod", 0)
    return mods


CLIENT_GRATITUDE = {
    "Chloe": [
        ("Burner Phone", "A Nokia with one contact: 'DO NOT ANSWER'.", 0, 0),
        ("Basilica WiFi Password", "Guest network: H0LYR0LL3R42", 0, 5),
    ],
    "Bobbie": [
        ("Dale Earnhardt Keychain", "Rubber. Sacred. Smells like 1998.", 0, 10),
        ("VHS: Best of NASCAR '97", "Three hours. Unskippable.", 5, 0),
    ],
    "Liam": [
        ("Artisan Salt", "Himalayan. $18 at the store. Liam got it free.", 0, 3),
        ("Vinyl: Band That Broke Up", "They reunite next week. You feel old.", 0, 15),
    ],
    "Mrs. Higgins": [
        ("Mystery Stew", "You don't ask. It's good. (+25 HP)", 25, 0),
        ("Sweet Potato Pie", "Grandma strength. (+15 HP, -10 Stress)", 15, 10),
    ],
    "Tyler": [
        ("Expired Bus Pass", "Still works somehow. (-$2 travel once)", 0, 0),
        ("Adderall? No — Herbal Tea", "It's just tea. (+5 HP)", 5, 5),
    ],
    "DeShawn": [
        ("Tenant Union Flyer", "You feel morally taller.", 0, 20),
        ("Hot Plate from Community Kitchen", "Real food. (+20 HP)", 20, 5),
    ],
    "Grandma Roz": [
        ("Brady Street VIP Stamp", "One free cover charge. Somewhere.", 0, 10),
        ("Old Fashioned Recipe", "Whiskey, sugar, bitters, Wisconsin.", 0, 15),
    ],
    "Mikey": [
        ("Elote Seasoning Packet", "Chili, lime, cotija vibes.", 10, 5),
        ("Mitchell Street Loyalty Card", "Buy 9 elotes, get judgment free.", 0, 0),
    ],
    "Pastor Dale": [
        ("Fish Fry To-Go Box", "Friday energy on a Tuesday.", 30, 10),
        ("Church Bulletin", "Potluck Saturday. You are invited.", 0, 8),
    ],
    "Jen": [
        ("Harbor District Parking Pass", "Stolen from a yacht. Feels wrong. Feels right.", 0, 5),
        ("Craft Beer Nobody Asked For", "IPA named 'Gentrification Tears'.", 0, 12),
    ],
}


def roll_gratitude(client_name: str, trust: int) -> Optional[Item]:
    """After crisis, chance for weird gratitude item scaled by trust."""
    table = CLIENT_GRATITUDE.get(client_name, [])
    if not table:
        return None
    chance = 0.35 + min(trust, 10) * 0.05
    if random.random() > chance:
        return None
    name, desc, hp, stress = random.choice(table)
    return Item(name, desc, 0, hp, stress)


# Side quests (simple flag-based)
SIDE_QUESTS = {
    "pothole_petition": {
        "title": "Mrs. Higgins' Pothole Petition",
        "client": "Mrs. Higgins",
        "neighborhood": "Sherman Park",
        "steps": ["get_signatures", "deliver_city_hall"],
        "reward_hours": 4.0,
        "reward_rep": 3,
    },
    "pierogi_delivery": {
        "title": "Chloe's Pierogi Run",
        "client": "Chloe",
        "neighborhood": "Polonia",
        "steps": ["pickup_basilica", "deliver_chloe"],
        "reward_hours": 3.0,
        "reward_rep": 2,
    },
    "elote_peace": {
        "title": "Mikey's Cart Truce",
        "client": "Mikey",
        "neighborhood": "Mitchell Street",
        "steps": ["talk_mikey", "talk_rival_cart"],
        "reward_hours": 2.5,
        "reward_rep": 2,
    },
}


def advance_quest(game_state, quest_id: str, step: str) -> Tuple[bool, str]:
    """
    Advance a side quest step. Returns (completed, message).
    """
    q = SIDE_QUESTS.get(quest_id)
    if not q:
        return False, "Unknown quest."
    progress = game_state.quest_progress.get(quest_id, [])
    if step in progress:
        return False, "Already did that."
    progress.append(step)
    game_state.quest_progress[quest_id] = progress
    if len(progress) >= len(q["steps"]):
        game_state.active_quest = None
        return True, f"QUEST COMPLETE: {q['title']}"
    return False, f"Quest updated: {q['title']} ({len(progress)}/{len(q['steps'])})"


def process_weighted_encounter(encounter_key: str, player, game_state) -> str:
    """Apply mechanical effects for structured encounters. Returns extra flavor."""
    fx = ENCOUNTER_EFFECTS.get(encounter_key, {})
    lines = []

    if fx.get("stress"):
        if fx["stress"] > 0:
            player.stress = min(player.max_stress, player.stress + fx["stress"])
            lines.append(f"Stress +{fx['stress']}.")
        else:
            player.relax(-fx["stress"])
            lines.append(f"Stress {fx['stress']}.")

    if fx.get("hp"):
        if fx["hp"] < 0:
            player.hp = max(1, player.hp + fx["hp"])
        else:
            player.heal(fx["hp"])
        lines.append(f"HP change: {fx['hp']}.")

    if fx.get("money"):
        player.modify_money(fx["money"])
        lines.append(f"Money change: ${fx['money']}.")

    if fx.get("text_extra"):
        lines.append(fx["text_extra"])

    if fx.get("reputation_bonus"):
        game_state.reputation_414 += fx["reputation_bonus"]

    return " ".join(lines) if lines else ""


# --- 414 REPUTATION PERKS ---
REPUTATION_PERKS = {
    5: "Bus drivers nod at you. Small win.",
    10: "El Trucko gives you the 'local' price (10% off next food truck visit).",
    15: "Crisis spawn rate drops slightly. The city respects you.",
    25: "Milverine intervention chance +3%. Legends recognize legends.",
    40: "You can skip one client cooldown per game (not implemented yet — vibes only).",
}


def get_reputation_title(rep: int) -> str:
    if rep >= 40:
        return "Honorary Milverine"
    if rep >= 25:
        return "Street Legend"
    if rep >= 15:
        return "Neighborhood Fixture"
    if rep >= 5:
        return "Regular at Wolski's"
    return "New Case Worker"


# --- TALLBOY V2 (Milwaukee Curve) ---
TALLBOY_PHASES = ("FRESH", "SIPPING", "BUZZED", "PEAK", "CRASHING", "EMPTY")


def open_tallboy_bag(player) -> Optional[str]:
    """Voluntary or forced bag open."""
    tb = player.tallboy_state
    if not tb or tb.get("phase") != "FRESH":
        return None
    tb["phase"] = "SIPPING"
    player.hp = max(1, player.hp - 2)
    player.relax(5)
    return "You open the bag. The illusion of discretion dies. Drinking in public: activated."


def tallboy_npc_reaction(client_name: str, phase: str, location: str) -> Optional[str]:
    reactions = {
        ("Bobbie", "FRESH"): "Bobbie salutes the bag. 'Respect. LakeFrontier before noon.'",
        ("Bobbie", "PEAK"): "Bobbie offers you a Dale Earnhardt plate to use as a coaster.",
        ("Mrs. Higgins", "FRESH"): "Mrs. Higgins squints. 'Child, I know what's in that bag.'",
        ("Mrs. Higgins", "SIPPING"): "She shakes her head but offers you pie anyway.",
        ("Tyler", "PEAK"): "Tyler thinks you're 'chill' and asks if you want to go to Deep Thought.",
        ("Grandma Roz", "SIPPING"): "Roz pours you water. 'Pace yourself, hon.'",
        ("DeShawn", "CRASHING"): "DeShawn hands you a flyer. 'Hydrate. Organize later.'",
        ("Jen", "FRESH"): "Jen whispers: 'HR can't see you from the harbor.'",
        ("Liam", "PEAK"): "Liam judges your craft beer choice in the bag. It's not craft. He respects it.",
        ("Chloe", "PEAK"): "Chloe: 'Bold of you to debug production while drinking.'",
    }
    return reactions.get((client_name, phase))


def advance_tallboy(player, blocks=0, talked=False, location: str = "") -> List[str]:
    """Full Milwaukee Curve state machine. Returns flavor lines."""
    if not player.tallboy_state:
        return []
    tb = player.tallboy_state
    tb["blocks"] = tb.get("blocks", 0) + blocks
    if talked:
        tb["people"] = tb.get("people", 0) + 1
    phase = tb.get("phase", "FRESH")
    lines = []

    if phase == "SIPPING" and tb["blocks"] >= 2:
        tb["phase"] = "BUZZED"
        player.relax(15)
        lines.append("The Buzz: stress melts. The caseload feels manageable. It isn't.")

    elif phase == "BUZZED" and talked and tb["people"] >= 1:
        tb["phase"] = "PEAK"
        player.heal(5)
        player.relax(10)
        lines.append("Peak Drunk: you text your ex about fish fry. You apply for a job you're not qualified for.")

    elif phase == "PEAK" and tb["blocks"] >= 5:
        if tb.get("second_tallboy"):
            tb["blocks"] = 3  # delay crash
            tb["second_tallboy"] = False
            lines.append("Second tallboy acquired. Crash postponed. Authentic Milwaukee harm reduction.")
        else:
            tb["phase"] = "CRASHING"
            player.stress = min(player.max_stress, player.stress + 20)
            player.hp = max(1, player.hp - 5)
            lines.append("The Crash: reality returns. Your inbox has 47 unread emails.")

    elif phase == "CRASHING" and tb["blocks"] >= 7:
        tb["phase"] = "EMPTY"
        lines.append("The can is empty. Pour one out or recycle. Headache included.")

    return lines


def buy_second_tallboy(player) -> bool:
    """While crashing, another tallboy delays the inevitable."""
    if player.tallboy_state and player.tallboy_state.get("phase") in ("PEAK", "CRASHING"):
        player.tallboy_state["second_tallboy"] = True
        player.tallboy_state["phase"] = "BUZZED"
        player.tallboy_state["blocks"] = 0
        return True
    return False


def can_dispose_tallboy(player) -> bool:
    tb = player.tallboy_state or {}
    return tb.get("phase") == "EMPTY" and tb.get("people", 0) >= 2


def dispose_tallboy(player, pour_out=False) -> Tuple[bool, str]:
    if not can_dispose_tallboy(player):
        if (player.tallboy_state or {}).get("phase") == "EMPTY":
            return False, "Talk to more people while emptying the bag. Milwaukee requires witnesses."
        return False, "Finish the Milwaukee Curve first."
    player.held_item = None
    player.tallboy_state = None
    player.relax(5)
    if pour_out:
        return True, "You pour one out for the dead homies. The bag goes in recycling. Respect."
    return True, "You recycle the can. Slight headache. Worth it."


def tick_global_story(game_state, turn_count: int) -> Optional[str]:
    """Rare world events — e.g. Deep Thought finally towed."""
    if game_state.flags.get("boat_removed"):
        return None
    if turn_count > 30 and random.random() < 0.03:
        game_state.flags["boat_removed"] = True
        return (
            "BREAKING: Deep Thought was towed across the Hoan Bridge. "
            "The city feels empty. Someone plays taps on a kazoo at Bradford Beach."
        )
    return None


# --- MORE SIDE QUESTS ---
SIDE_QUESTS["boat_pilgrimage"] = {
    "title": "Last Visit to Deep Thought",
    "client": None,
    "neighborhood": "East Side",
    "steps": ["visit_boat", "take_photo", "witness_removal"],
    "reward_hours": 2.0,
    "reward_rep": 5,
}

SIDE_QUESTS["winter_survival"] = {
    "title": "Survive a Milwaukee Winter Week",
    "client": None,
    "neighborhood": "Sherman Park",
    "steps": ["survive_parking_ban", "survive_snow_emergency", "still_working"],
    "reward_hours": 3.0,
    "reward_rep": 4,
}

SIDE_QUESTS["tyler_rave_rescue"] = {
    "title": "Find Tyler in The Rave Basement",
    "client": "Tyler",
    "neighborhood": "Near West Side",
    "steps": ["enter_rave", "search_pool", "escort_tyler_out"],
    "reward_hours": 3.5,
    "reward_rep": 3,
}
