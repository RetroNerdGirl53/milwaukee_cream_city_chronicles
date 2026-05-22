"""
food_quests.py - Multi-step food arcs tied to real Milwaukee restaurant lore.
"""

from typing import Dict, Tuple, Optional
import world_events
from food_lore import random_chatter

# Merged into world_events.SIDE_QUESTS on import
FOOD_QUESTS: Dict[str, Dict] = {
    "malt_and_mayor": {
        "title": "The Malt & The Mayor (Miss Katie's)",
        "neighborhood": "Near West Side",
        "landmark": "Miss Katie's Diner",
        "client": "Tyler",
        "steps": ["order_malt", "selfie_with_cutout", "deliver_comfort"],
        "reward_hours": 4.0,
        "reward_rep": 4,
        "intro": "Tyler is stressed about politics in his feed. Mrs. Higgins says: 'Take that boy a malt from Miss Katie's — presidents ate there.'",
    },
    "mild_sauce_run": {
        "title": "JJ's Mild Sauce Run",
        "neighborhood": "Bronzeville",
        "landmark": "JJ Fish & Chicken (35th St)",
        "client": "DeShawn",
        "steps": ["buy_snack_box_35th", "buy_snack_box_capitol", "deliver_deShawn"],
        "reward_hours": 3.0,
        "reward_rep": 3,
        "intro": "DeShawn is feeding tenant meeting volunteers. He needs JJ's Snack Boxes from two locations. Yes, two.",
    },
    "gold_rush_pilgrimage": {
        "title": "Gold Rush Pilgrimage",
        "neighborhood": "Bronzeville",
        "landmark": "Gold Rush Chicken (North Ave — Closed)",
        "client": "Bobbie",
        "steps": ["visit_ghost_north", "visit_howell_bucket", "tell_bobbie"],
        "reward_hours": 2.5,
        "reward_rep": 3,
        "intro": "Bobbie won't stop talking about the old Gold Rush on North Ave. He needs you to visit the ghost sign, then get a real bucket on Howell.",
    },
    "pizza_puff_pilgrimage": {
        "title": "Fryerz Pizza Puff Pilgrimage",
        "neighborhood": "Amani",
        "landmark": "Fryerz",
        "client": "Tyler",
        "steps": ["survive_parking", "order_puff", "deliver_tyler"],
        "reward_hours": 2.0,
        "reward_rep": 2,
        "intro": "Tyler discovered Fryerz pizza puffs on TikTok. His thesis can wait. Your caseload cannot.",
    },
    "ians_thesis_slices": {
        "title": "Ian's Mac n Cheese Intervention",
        "neighborhood": "East Side",
        "landmark": "Ian's Pizza (North Ave)",
        "client": "Tyler",
        "steps": ["buy_mac_slice", "buy_second_slice", "deliver_tyler"],
        "reward_hours": 2.0,
        "reward_rep": 2,
        "intro": "Tyler has a 40-page thesis due. He requires Ian's Mac n Cheese pizza. Food Network said it's legal.",
    },
    "shuttle_4am": {
        "title": "Pizza Shuttle Mercy Run",
        "neighborhood": "Brady Street",
        "landmark": "Pizza Shuttle (Farwell)",
        "client": "Mrs. Higgins",
        "steps": ["order_shuttle", "order_wings", "deliver_higgins"],
        "reward_hours": 3.0,
        "reward_rep": 3,
        "intro": "Mrs. Higgins called at 11pm. She wants Pizza Shuttle breadsticks and wings. Winston the driver may save your soul.",
    },
    "buffet_intervention": {
        "title": "27th Street Buffet Intervention",
        "neighborhood": "Mitchell Street",
        "landmark": "New China Buffet (27th St)",
        "client": "Mrs. Higgins",
        "steps": ["lunch_buffet", "avoid_sushi", "escort_higgins_out"],
        "reward_hours": 2.5,
        "reward_rep": 2,
        "intro": "Mrs. Higgins insists on New China Buffet on 27th for her birthday. Your job: survive styrofoam, hunt fresh crab, no metal in egg rolls.",
    },
    "big_shark_return": {
        "title": "Big Shark Homecoming",
        "neighborhood": "Bronzeville",
        "landmark": "Big Sharks (North Ave)",
        "client": "Bobbie",
        "steps": ["order_italian_beef", "order_onion_rings", "share_bobbie"],
        "reward_hours": 2.0,
        "reward_rep": 2,
        "intro": "Bobbie hasn't had Big Sharks Italian beef since 2010. Yelp says someone cried after 14 years. Help him home.",
    },
    "double_clock_lunch": {
        "title": "George Webb's Clock Orientation",
        "neighborhood": "Downtown",
        "landmark": "George Webb's (Wells St)",
        "client": None,
        "steps": ["two_burgers", "explain_clocks", "report_center"],
        "reward_hours": 1.5,
        "reward_rep": 2,
        "intro": "The Center wants new hires to learn Milwaukee. Buy George Webb's 2 burgers. Explain the two clocks. Try not to cry.",
    },
    "custard_truce": {
        "title": "The Custard Truce (Culver's vs Kopp's)",
        "neighborhood": "Bay View",
        "landmark": "Culver's (Kinnickinnic)",
        "client": "Liam",
        "steps": ["culvers_concrete", "kopps_scoop", "judge_liam"],
        "reward_hours": 2.0,
        "reward_rep": 3,
        "intro": "Liam and a Bay View influencer are feuding: Culver's vs Kopp's. Eat both. Judge. Milwaukee needs peace.",
    },
}


def register_food_quests():
    for qid, q in FOOD_QUESTS.items():
        if qid not in world_events.SIDE_QUESTS:
            world_events.SIDE_QUESTS[qid] = q


register_food_quests()


def get_active_food_quest(game_state) -> Optional[Dict]:
    aq = game_state.active_quest
    if aq in FOOD_QUESTS:
        return FOOD_QUESTS[aq]
    return None


def advance_food_quest_step(game_state, quest_id: str, step: str) -> Tuple[bool, str]:
    return world_events.advance_quest(game_state, quest_id, step)


def handle_food_quest_at_landmark(player, game_state, landmark: str, item_ordered: str = "") -> Optional[str]:
    """
    Call after visiting a food landmark / ordering. Returns flavor text if quest advanced.
    """
    aq = game_state.active_quest
    if aq not in FOOD_QUESTS:
        return None
    q = FOOD_QUESTS[aq]
    if q.get("landmark") != landmark and aq not in (
        "mild_sauce_run",
        "custard_truce",
    ):
        return None
    progress = game_state.quest_progress.get(aq, [])
    lines = []

    if aq == "malt_and_mayor" and landmark == "Miss Katie's Diner":
        if "order_malt" not in progress and "malt" in item_ordered.lower():
            advance_food_quest_step(game_state, aq, "order_malt")
            lines.append("You sip a homemade malt. Hillary's cutout nods approvingly.")
        elif "order_malt" in progress and "selfie_with_cutout" not in progress:
            if input("Take a selfie with the political cutouts? (y/n) > ").lower() == "y":
                advance_food_quest_step(game_state, aq, "selfie_with_cutout")
                lines.append("Posted. Tyler texts: 'why is Michelle Obama in your break room'")

    elif aq == "mild_sauce_run" and "JJ Fish" in landmark:
        if "35th" in landmark and "buy_snack_box_35th" not in progress:
            if "Snack" in item_ordered or "Combo" in item_ordered:
                advance_food_quest_step(game_state, aq, "buy_snack_box_35th")
                lines.append("35th St JJ Snack Box acquired. Mild sauce sealed for justice.")
        elif "Capitol" in landmark and "buy_snack_box_capitol" not in progress and "buy_snack_box_35th" in progress:
            if "Snack" in item_ordered or "Fish" in item_ordered or "Combo" in item_ordered:
                advance_food_quest_step(game_state, aq, "buy_snack_box_capitol")
                lines.append("Capitol Dr JJ secured. DeShawn's volunteers will eat.")

    elif aq == "gold_rush_pilgrimage":
        if landmark == "Gold Rush Chicken (North Ave — Closed)" and "visit_ghost_north" not in progress:
            advance_food_quest_step(game_state, aq, "visit_ghost_north")
            lines.append("You pay respects to the yellow siding ghost. Bobbie would be proud.")
        elif landmark == "Gold Rush Chicken (Howell)" and "visit_ghost_north" in progress and "visit_howell_bucket" not in progress:
            if "Bucket" in item_ordered or "Chicken" in item_ordered:
                advance_food_quest_step(game_state, aq, "visit_howell_bucket")
                lines.append("Real Gold Rush bucket obtained. The pilgrimage is complete.")

    elif aq == "pizza_puff_pilgrimage" and landmark == "Fryerz":
        if "survive_parking" not in progress:
            advance_food_quest_step(game_state, aq, "survive_parking")
            lines.append("You survived Fryerz parking. Yelp warned you. You prevailed.")
        elif "order_puff" not in progress and "Puff" in item_ordered:
            advance_food_quest_step(game_state, aq, "order_puff")
            lines.append("Pizza puff secured. Tyler's TikTok hunger grows.")

    elif aq == "ians_thesis_slices" and "Ian's" in landmark:
        if "Mac" in item_ordered:
            if "buy_mac_slice" not in progress:
                advance_food_quest_step(game_state, aq, "buy_mac_slice")
                lines.append("First Mac n Cheese slice down. Food Network approved this coping mechanism.")
            elif "buy_second_slice" not in progress:
                advance_food_quest_step(game_state, aq, "buy_second_slice")
                lines.append("Second slice acquired. Thesis still not written.")

    elif aq == "shuttle_4am" and "Pizza Shuttle" in landmark:
        if "order_shuttle" not in progress and ("Shuttle" in item_ordered or "CYO" in item_ordered or "Slice" in item_ordered):
            advance_food_quest_step(game_state, aq, "order_shuttle")
            lines.append("Shuttle order placed. Winston may deliver your destiny.")
        elif "order_wings" not in progress and ("Wing" in item_ordered or "Breadstick" in item_ordered):
            advance_food_quest_step(game_state, aq, "order_wings")
            lines.append("Wings 9.3 energy acquired for Mrs. Higgins.")

    elif aq == "buffet_intervention" and landmark == "New China Buffet (27th St)":
        if "lunch_buffet" not in progress and "Buffet" in item_ordered:
            advance_food_quest_step(game_state, aq, "lunch_buffet")
            lines.append("You enter the buffet. Styrofoam plate. Steel yourself.")
        elif "avoid_sushi" not in progress and "lunch_buffet" in progress:
            advance_food_quest_step(game_state, aq, "avoid_sushi")
            lines.append("You skipped the sushi. Jaw tingling avoided. Hero.")
        elif "escort_higgins_out" not in progress and "avoid_sushi" in progress:
            advance_food_quest_step(game_state, aq, "escort_higgins_out")
            lines.append("Mrs. Higgins leaves happy. No twist ties found.")

    elif aq == "big_shark_return" and landmark == "Big Sharks (North Ave)":
        if "order_italian_beef" not in progress and ("Italian" in item_ordered or "beef" in item_ordered.lower()):
            advance_food_quest_step(game_state, aq, "order_italian_beef")
            lines.append("'OMG they rocked my soul' — Bobbie's words, not yours. Yet.")
        elif "order_onion_rings" not in progress and ("Ring" in item_ordered or "Nachos" in item_ordered):
            advance_food_quest_step(game_state, aq, "order_onion_rings")
            lines.append("Onion rings complete the homecoming arc.")

    elif aq == "double_clock_lunch" and landmark == "George Webb's (Wells St)":
        if "two_burgers" not in progress and "Burger" in item_ordered:
            advance_food_quest_step(game_state, aq, "two_burgers")
            lines.append("Two burgers acquired. The clocks disagree by one minute.")
        elif "explain_clocks" not in progress and "two_burgers" in progress:
            advance_food_quest_step(game_state, aq, "explain_clocks")
            lines.append("You explained 23:59:59 to an imaginary trainee. Nailed it.")

    elif aq == "custard_truce":
        if "culvers_concrete" not in progress and landmark == "Culver's (Kinnickinnic)" and (
            "Concrete" in item_ordered or "Custard" in item_ordered or "Mint" in item_ordered
        ):
            advance_food_quest_step(game_state, aq, "culvers_concrete")
            lines.append("Culver's concrete logged. Kopp's awaits.")
        elif "kopps_scoop" not in progress and "Kopp" in landmark and (
            "Scoop" in item_ordered or "Sundae" in item_ordered
        ):
            advance_food_quest_step(game_state, aq, "kopps_scoop")
            lines.append("Kopp's scoop logged. Liam awaits judgment.")

    if not lines:
        return None

    # Check completion
    progress = game_state.quest_progress.get(aq, [])
    if len(progress) >= len(q["steps"]):
        game_state.active_quest = None
        player.add_billable_hours(q["reward_hours"])
        game_state.reputation_414 += q["reward_rep"]
        lines.append(f"QUEST COMPLETE: {q['title']}")
        return "\n".join(lines)
    return "\n".join(lines)


def handle_food_quest_client_delivery(player, game_state, client_name: str) -> Optional[str]:
    """Complete quests that need delivering to a client in their neighborhood."""
    aq = game_state.active_quest
    if not aq or aq not in FOOD_QUESTS:
        return None
    q = FOOD_QUESTS[aq]
    if q.get("client") != client_name:
        return None
    progress = game_state.quest_progress.get(aq, [])
    final_steps = {
        "malt_and_mayor": ("deliver_comfort", "selfie_with_cutout"),
        "mild_sauce_run": ("deliver_deShawn", "buy_snack_box_capitol"),
        "gold_rush_pilgrimage": ("tell_bobbie", "visit_howell_bucket"),
        "pizza_puff_pilgrimage": ("deliver_tyler", "order_puff"),
        "ians_thesis_slices": ("deliver_tyler", "buy_second_slice"),
        "shuttle_4am": ("deliver_higgins", "order_wings"),
        "buffet_intervention": ("escort_higgins_out", "avoid_sushi"),
        "big_shark_return": ("share_bobbie", "order_onion_rings"),
        "custard_truce": ("judge_liam", "kopps_scoop"),
    }
    if aq not in final_steps:
        return None
    step, prereq = final_steps[aq]
    if prereq not in progress or step in progress:
        return None
    if input(f"Complete delivery for '{q['title']}'? (y/n) > ").lower() != "y":
        return None
    done, msg = advance_food_quest_step(game_state, aq, step)
    out = [msg]
    if done:
        player.add_billable_hours(q["reward_hours"])
        game_state.reputation_414 += q["reward_rep"]
    return "\n".join(out)


def print_quest_intro(quest_id: str):
    q = FOOD_QUESTS.get(quest_id)
    if q and q.get("intro"):
        print(q["intro"])
