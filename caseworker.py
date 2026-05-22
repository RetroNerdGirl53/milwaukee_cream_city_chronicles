import random
import time
import sys
import os
import pantheon
import economy
import combat
from engine import Player, GameState, Client, Item
from world_data import MILWAUKEE_MAP, TravelCost, GENTRIFIED_NEIGHBORHOODS
from food_places import FOOD_MENUS, FOOD_FLAVOR
import food_quests
from food_lore import random_chatter
from food_quests import (
    FOOD_QUESTS,
    handle_food_quest_at_landmark,
    handle_food_quest_client_delivery,
    print_quest_intro,
)
from text_assets import (
    CLIENT_SCENARIOS, LANDMARK_FLAVOR, RANDOM_ENCOUNTERS, ASCII_ART,
    CLIENT_DEEP_TALK, MILWAUKEE_LORE_SNIPPETS,
)

LANDMARK_FLAVOR = {**LANDMARK_FLAVOR, **FOOD_FLAVOR}
import world_events
from graphics import Colors, clear_screen, typewriter_print, print_centered, print_banner, print_separator
from save_system import (
    save_game, load_game, list_save_slots, delete_save,
    token_registry, verify_token
)
from sourdough import sourdough_manager, acquire_starter, FORM_PARTNER
from tumbleweave import check_tumbleweave_encounter, start_tumbleweave_battle, TUMBLEWEAVE_TOKEN_CONFIG

# --- THE SACRED TEXTS ---
def play_intro():
    clear_screen()
    print(Colors.PINK + ASCII_ART['TITLE'] + Colors.RESET)
    time.sleep(1)

    print_separator(color=Colors.PINK)
    typewriter_print("IN THE BEGINNING, THERE WAS THE MILVERINE.", color=Colors.CYAN)
    typewriter_print("He walked the 414 when others drove. He wore the shorts in January.", color=Colors.WHITE)
    typewriter_print("He did not have claws because he did not need them.", color=Colors.WHITE)
    print("")
    typewriter_print("AND IN THE SHADOWS, THERE WAS KENNEDY.", color=Colors.MAGENTA)
    typewriter_print("The Sorceress of the System. The High Priestess of 'Per My Last Email'.", color=Colors.WHITE)
    typewriter_print("The Bane of red tape. Destroyer of administrations. Dark lord of the case load", color=Colors.WHITE)
    print("")
    print_banner("WELCOME TO MILWAUKEE", color=Colors.HOT_PINK)
    typewriter_print("Where the beer is cold, the cheese is loud, and the bureaucracy is hungry.", color=Colors.TEAL)
    print_separator(color=Colors.PINK)
    time.sleep(2)

# --- THE MENUS (SATIRE EDITION) ---
# Global instance for the food truck so state persists (hype)
el_trucko = economy.FoodTruck("El Trucko", {"Street Tacos": 3.50, "Elotes": 4.00, "Jarritos": 2.50})

landmark_menus = {
    "Sobelman's": {
        "Bloody Masterpiece": (25.00, 10, 50, "A garnish that defies physics. Basically a salad with vodka."),
        "Cheese Balls": (9.00, 5, 5, "Grease is a love language."),
        "Friday Fish Fry": (14.00, 30, 10, "It's Friday somewhere. Beer battered cod, potato pancakes, coleslaw. The holy trinity.")
    },
    "Real Chili": {
        "Marquette Special": (9.50, 20, 0, "Spaghetti and beans. Fuel for the sleep-deprived."),
        "Tums Garnish": (1.00, 0, 5, "You'll need it.")
    },
    "Safe House": {
        "Spy Burger": (14.00, 15, 5, "You pay extra for the secret door."),
        "Cover Charge": (5.00, 0, 0, "The price of not knowing the password.")
    },
    "The Vanguard": {
        "Duck BLT Sausage": (12.00, 15, 10, "Fancy meat served on a tray. Very Bay View."),
        "Shot of Malort": (5.00, -5, 20, "Tastes like gasoline and bad decisions. Clears the sinuses.")
    },
    "Speed Queen BBQ": {
        "Rib Tips": (18.00, 40, 5, "The smoke smell alone heals your soul."),
        "White Bread Slice": (0.50, 2, 0, "The edible napkin.")
    },
    "Conejito's Place": {
        "Plate Lunch": (8.00, 20, 5, "served on a paper plate. Cheap and glorious."),
        "Margarita": (6.00, 0, 10, "Effective.")
    },
    "Leon's Frozen Custard": {
        "Butter Pecan": (4.50, 5, 15, "Frozen gold. The neon lights soothe you."),
        "Spanish Hamburger": (4.50, 10, 0, "It's a sloppy joe. Don't ask questions.")
    },
    "Central Library": {
        "Ancient Coffee": (5.00, 5, 5, "Black as the void. Required for summoning Kennedy."),
        "Forbidden Form 1040-X": (10.00, 0, 0, "A tax amendment from 1994. Ritual item.")
    },
    "Wolski's": {
        "The Closer": (7.00, 0, 20, "You stay until the bar closes. You get a sticker that says you survived."),
        "Popcorn": (0.00, 2, 0, "It's free and salty."),
        "Friday Fish Fry": (13.00, 30, 15, "Perch or cod? The eternal question. Served with rye bread and tartar.")
    },
    "Stop-N-Rob": {
        "Flamin Hot Cheez-eee-tos": (1.50, 0, 25, "It's spicy, cheaper than name brand, gives you the shits, and is full of oh so many good memories"),
        "Last Weeks Coffee": (.50, -5, 30, "It's old, fast, and tastes like it but it does the job for cheap"),
        "Tall Boy": (2.00, -10, 20, "Beer. In a tall can. LakeFrontier Breweries. Brown paper bag. Everyone knows. The bag fools nobody."),
        "Glass Pipe": (5.00, -2, 200, "A glass pipe for all your Canna...err tobacco products. The cashier hints that it comes with a free sample"),
        "Giga-N-to Green Energy": (4.00, 20, -20, "Standard energy drink in a tallboy can. You guy always gives you a good deal"),
        "Hoho's": (1.50, 3, 5, "HoHo (Singles) - Separated from its family and marked up 900%. The American dream tastes like chocolate and exploitation."),
    },
    "Harbor House": {
        "Lake Trout": (22.00, 20, 5, "You eat while yachts judge your credit score."),
        "Old Fashioned": (11.00, 0, 12, "Wisconsin's state cocktail. Sweet, strong, honest."),
    },
    "Coffee Makes You Black": {
        "House Coffee": (3.00, 5, 8, "Strong. Community-roasted vibes."),
        "Sweet Potato Pie Slice": (4.00, 12, 10, "Mrs. Higgins would approve."),
    },
    "Art Bar": {
        "PBR Tall Boy": (3.00, -5, 15, "Brady Street currency."),
        "Karaoke Courage Shot": (6.00, 0, 25, "You will regret singing. You will do it anyway."),
    },
    "Glory Days": {
        "Bon Jovi Nightcap": (5.00, 0, 18, "Livin' on a Prayer. Dying on a caseload."),
    },
    "Gee's Clippers": {
        "Lineup + Life Advice": (25.00, 5, 20, "You leave looking sharp and emotionally seen."),
    },
    "Milwaukee Public Market": {
        "Sample Everything": (0.00, 5, 5, "You ate seventeen samples. Bought nothing. Classic."),
        "Artisan Olive Oil": (14.00, 0, 8, "Third Ward prices. Your wallet weeps."),
    },
    "Basilica of St. Josaphat": {
        "Candle Donation": (2.00, 0, 15, "Peace. Incense. Chloe might be in the basement."),
        "Pierogi Plate": (8.00, 20, 10, "Fundraiser pierogis hit the soul."),
    },
    "Polish Center of Wisconsin": {
        "Kielbasa Plate": (10.00, 25, 5, "South Side holy food."),
    },
    "Falcon Bowl": {
        "Cheap Pitcher": (8.00, -5, 20, "Riverwest bowling therapy."),
    },
    "Washington Park": {
        "Bench Therapy": (0.00, 0, 12, "You watch geese. They watch you. Mutual respect."),
    },
    "Deep Thought": {
        "Pilgrimage Photo": (0.00, 0, 15, "You visited the beached boat. SS Milwaukee energy. No admission fee. Maximum lore."),
        "Leave Graffiti": (0.00, 0, 8, "You tag the hull with something respectful-ish. The city will remove the boat before they remove this."),
        "Watch Salvage Fail": (0.00, 5, 20, "A tow truck tries. The boat stays. Milwaukee wins again."),
    },
    "Deer District": {
        "Bucks Watch Party Pretzel": (9.00, 10, 5, "Fiserv adjacent. Loud. Joyful. Expensive."),
        "Anthem Loud": (0.00, 0, 8, "You stand up. You don't know why. You feel pride."),
    },
    "The Rave": {
        "GA Ticket (All Ages)": (35.00, 0, 25, "Sticky floor. Unknown openers. Core memory unlocked."),
        "Venue Water Bottle": (12.00, 2, 0, "Twelve dollars. Hydration as luxury good."),
        "Merch Table Hoodie": (45.00, 0, 10, "Band name you discovered tonight. Will age beautifully."),
    },
}
landmark_menus.update(FOOD_MENUS)

def is_fish_fry_day():
    """Check if today is Friday (or if we want to allow Fish Fry any day for gameplay)."""
    import datetime
    return datetime.datetime.now().weekday() == 4  # Friday is 4

def check_fish_fry(location_name):
    """Returns True if this location should offer Fish Fry today."""
    # Always allow Fish Fry for gameplay purposes, but mark it specially
    fish_fry_locations = ["Sobelman's", "Wolski's", "Real Chili", "Speed Queen BBQ", "Ma Fischer's (Brady St)"]
    return location_name in fish_fry_locations

# --- INITIALIZATION HELPER ---
def init_game_state(player):
    """
    Initializes the GameState and populates the ClientRoster based on TEXT_ASSETS and MILWAUKEE_MAP.
    """
    gs = GameState()

    # Map clients to neighborhoods based on world_data or text_assets
    # world_data.py doesn't list clients explicitly in the dict structure in the latest read,
    # but caseworker.py had them hardcoded.
    # text_assets.py has the scenarios.

    # We need to reconstruct the roster.
    # Based on the original caseworker.py:
    # Chloe -> Polonia
    # Bobbie -> West Allis
    # Liam -> Bay View
    # Mrs. Higgins -> Sherman Park
    # Tyler -> East Side

    # Let's use the keys from CLIENT_SCENARIOS
    client_locs = {
        "Chloe": "Polonia",
        "Bobbie": "West Allis",
        "Liam": "Bay View",
        "Mrs. Higgins": "Sherman Park",
        "Tyler": "East Side",
        "DeShawn": "Amani",
        "Grandma Roz": "Brady Street",
        "Mikey": "Mitchell Street",
        "Pastor Dale": "Bronzeville",
        "Jen": "Harbor District",
    }

    for name, loc in client_locs.items():
        c = Client(name, loc, "Chill")
        gs.client_roster.add_client(c)

    return gs

def get_client_enemy_data(client_name):
    """
    Returns the enemy data for a specific client (reconstructed from original caseworker.py).
    """
    if client_name == "Chloe":
        return {"name": "Sentient Roomba", "hp": 50, "weakness": "Logic"}
    elif client_name == "Bobbie":
        return {"name": "The Ticket Demon", "hp": 60, "weakness": "Paperwork"}
    elif client_name == "Liam":
        return {"name": "The Sourdough Monster", "hp": 45, "weakness": "Apathy"}
    elif client_name == "Mrs. Higgins":
        return {"name": "The City Inspector", "hp": 80, "weakness": "Paperwork"}
    elif client_name == "Tyler":
        return {"name": "The Chlorine Spirit", "hp": 50, "weakness": "Apathy"}
    elif client_name == "DeShawn":
        return {"name": "Slumlord LLC", "hp": 70, "weakness": "Paperwork"}
    elif client_name == "Grandma Roz":
        return {"name": "The Health Inspector", "hp": 55, "weakness": "Logic"}
    elif client_name == "Mikey":
        return {"name": "311 Karen", "hp": 45, "weakness": "Logic"}
    elif client_name == "Pastor Dale":
        return {"name": "Broken Fryer Gremlin", "hp": 50, "weakness": "Apathy"}
    elif client_name == "Jen":
        return {"name": "Yacht Party Planner Chad", "hp": 65, "weakness": "Apathy"}
    return {"name": "Generic Bureaucrat", "hp": 50, "weakness": "Paperwork"}

def get_client_scenarios(client_name, mood):
    """
    Returns the list of scenarios for a client based on mood from TEXT_ASSETS.
    """
    scenarios = CLIENT_SCENARIOS.get(client_name, [])
    # Filter by mood (Tuple: (Mood, Text))
    return [s[1] for s in scenarios if s[0] == mood]


def mint_collectible(player, token_name: str, item_desc: str, hp=0, stress=0):
    """Mint crypto token and add inventory item if supply allows."""
    token = token_registry.mint_token(token_name, player.name)
    if token:
        print(f"\n{Colors.CYAN}*** CRYPTO COLLECTIBLE ***{Colors.RESET}")
        print(f"Token ID: {token['token_id']} | {token['rarity']} | {token['supply_info']}")
        player.add_item(Item(token_name, item_desc, 0, hp, stress))
        return True
    print(Colors.BRIGHT_BLACK + f"{token_name} supply exhausted — you still did the thing." + Colors.RESET)
    return False


def print_tallboy_lines(lines):
    for line in lines:
        print(Colors.YELLOW + line + Colors.RESET)


def start_side_quest(game_state, quest_id):
    if quest_id in world_events.SIDE_QUESTS:
        game_state.active_quest = quest_id
        game_state.quest_progress[quest_id] = []
        return world_events.SIDE_QUESTS[quest_id]["title"]
    return None


def handle_quest_actions(player, game_state, curr_loc_name):
    """Optional quest step interactions at landmarks/clients."""
    aq = game_state.active_quest
    if not aq:
        return
    q = world_events.SIDE_QUESTS.get(aq)
    if not q:
        return
    progress = game_state.quest_progress.get(aq, [])
    if aq == "pothole_petition" and curr_loc_name == "Sherman Park" and "get_signatures" not in progress:
        if input("Gather signatures at Sherman Park? (y/n) > ").lower() == "y":
            done, msg = world_events.advance_quest(game_state, aq, "get_signatures")
            print(msg)
    elif aq == "pothole_petition" and curr_loc_name == "Downtown" and "get_signatures" in progress and "deliver_city_hall" not in progress:
        if input("Deliver petition to City Hall (Downtown)? (y/n) > ").lower() == "y":
            done, msg = world_events.advance_quest(game_state, aq, "deliver_city_hall")
            print(msg)
            if done:
                player.add_billable_hours(q["reward_hours"])
                game_state.reputation_414 += q["reward_rep"]
    elif aq == "pierogi_delivery" and curr_loc_name == "Polonia" and "pickup_basilica" not in progress:
        if input("Pick up pierogis at the Basilica? (y/n) > ").lower() == "y":
            done, msg = world_events.advance_quest(game_state, aq, "pickup_basilica")
            print(msg)
    elif aq == "pierogi_delivery" and curr_loc_name == "Polonia" and "pickup_basilica" in progress and "deliver_chloe" not in progress:
        clients = game_state.client_roster.get_clients_in_neighborhood("Polonia")
        if any(c.name == "Chloe" for c in clients):
            done, msg = world_events.advance_quest(game_state, aq, "deliver_chloe")
            print(msg)
            if done:
                player.add_billable_hours(q["reward_hours"])
                game_state.reputation_414 += q["reward_rep"]
    elif aq == "elote_peace" and curr_loc_name == "Mitchell Street":
        if "talk_mikey" not in progress:
            done, msg = world_events.advance_quest(game_state, aq, "talk_mikey")
            print(msg + " Mikey agrees to a ceasefire if the other cart moves 20 feet.")
        elif "talk_rival_cart" not in progress:
            done, msg = world_events.advance_quest(game_state, aq, "talk_rival_cart")
            print(msg)
            if done:
                player.add_billable_hours(q["reward_hours"])
                game_state.reputation_414 += q["reward_rep"]
    elif aq == "boat_pilgrimage" and curr_loc_name == "East Side":
        if "visit_boat" not in progress and not game_state.flags.get("boat_removed"):
            if input("Visit Deep Thought on the beach? (y/n) > ").lower() == "y":
                world_events.advance_quest(game_state, aq, "visit_boat")
                print("You touch the hull. It's barnacle and graffiti and love.")
        elif "visit_boat" in progress and "take_photo" not in progress:
            if input("Post the pilgrimage photo? (y/n) > ").lower() == "y":
                world_events.advance_quest(game_state, aq, "take_photo")
                mint_collectible(player, "Deep Thought Pilgrimage", "Proof you visited the Milwaukee boat.")
        elif game_state.flags.get("boat_removed") and "witness_removal" not in progress:
            done, msg = world_events.advance_quest(game_state, aq, "witness_removal")
            print(msg)
            if done:
                player.add_billable_hours(q["reward_hours"])
                game_state.reputation_414 += q["reward_rep"]
                mint_collectible(player, "Boat Removal Witness", "You saw it leave. RIP SS Milwaukee energy.", stress=20)
    elif aq == "winter_survival":
        pass  # advanced via encounters (see explore handler)
    elif aq == "tyler_rave_rescue" and curr_loc_name == "Near West Side":
        clients = game_state.client_roster.get_clients_in_neighborhood("East Side")
        tyler = next((c for c in clients if c.name == "Tyler"), None)
        if "escort_tyler_out" not in progress and tyler and tyler.mood == "Crisis":
            if "search_pool" in progress and input("Escort Tyler out of The Rave? (y/n) > ").lower() == "y":
                done, msg = world_events.advance_quest(game_state, aq, "escort_tyler_out")
                print(msg)
                if done:
                    q = world_events.SIDE_QUESTS[aq]
                    player.add_billable_hours(q["reward_hours"])
                    game_state.reputation_414 += q["reward_rep"]
                    tyler.set_mood("Chill")
                    player.update_client_relationship("Tyler", trust_change=2, set_cooldown=4)
        elif "enter_rave" not in progress:
            if input("Enter The Rave to look for Tyler? (y/n) > ").lower() == "y":
                world_events.advance_quest(game_state, aq, "enter_rave")
                print("You're in. Wisconsin Ave bass thumps. The basement awaits.")
    elif aq == "double_clock_lunch" and curr_loc_name == "The Center":
        if "explain_clocks" in progress and "report_center" not in progress:
            if input("Report George Webb clock orientation to The Center? (y/n) > ").lower() == "y":
                done, msg = world_events.advance_quest(game_state, aq, "report_center")
                print(msg)
                if done:
                    q = world_events.SIDE_QUESTS[aq]
                    player.add_billable_hours(q["reward_hours"])
                    game_state.reputation_414 += q["reward_rep"]


# --- GAME LOOP ACTIONS ---

def handle_crisis(player, client, game_state=None):
    """
    Handles the crisis combat loop.
    """
    clear_screen()
    print(Colors.RED + ASCII_ART['COMBAT'] + Colors.RESET)

    enemy_data = get_client_enemy_data(client.name)
    enemy = combat.Enemy(enemy_data["name"], combat.Enemy.TYPE_STONEWALLER, enemy_data["hp"])
    # Determine enemy type based on weakness/lore (Satire)
    if enemy_data['weakness'] == 'Logic': enemy.type = combat.Enemy.TYPE_STONEWALLER # Bureaucrats hate logic
    elif enemy_data['weakness'] == 'Apathy': enemy.type = combat.Enemy.TYPE_AGGRESSOR # Emotionals hate apathy
    elif enemy_data['weakness'] == 'Paperwork': enemy.type = combat.Enemy.TYPE_DRAINER # Paperwork drains you

    print_banner(f"CONFRONTING: {enemy.name}", color=Colors.RED)
    
    # Kennedy Check
    if player.has_item("Administrative Override"):
        print(Colors.style("\n[?] Invoke Kennedy's ADMINISTRATIVE OVERRIDE? (y/n)", color=Colors.MAGENTA))
        if input("> ") == "y":
            print(Colors.MAGENTA + "\n*** KENNEDY'S WRATH ***" + Colors.RESET)
            typewriter_print("A giant spectral rubber stamp descends from the sky.", color=Colors.PINK)
            print(Colors.style("IT READS: 'NOT MY PROBLEM'.", styles=[Colors.BOLD, Colors.UNDERLINE]))
            print(f"The {enemy.name} is instantly filed away.")
            player.remove_item("Administrative Override")
            player.exp += 50
            client.set_mood("Chill")
            return

    # Combat Loop
    while enemy.is_alive() and player.is_alive():
        print(f"{Colors.RED}Enemy HP: {enemy.hp}{Colors.RESET} | {Colors.MAGENTA}Your Stress: {player.stress}{Colors.RESET}")
        print(Colors.CYAN + "1. Malicious Compliance" + Colors.WHITE + " (Use rules against them)")
        print(Colors.CYAN + "2. Weaponized Apathy" + Colors.WHITE + " (Stare blankly)")
        print(Colors.CYAN + "3. Bureaucratic Jargon" + Colors.WHITE + " (Confuse them)")
        print(Colors.CYAN + "4. 'The Ope'" + Colors.WHITE + " (Dodge)")
        print(Colors.CYAN + "5. Contextual Move" + Colors.RESET)
        
        try:
            choice = input(Colors.YELLOW + "> " + Colors.RESET)
            move = ""
            if choice == "1": move = combat.MOVE_MALICIOUS_COMPLIANCE
            elif choice == "2": move = combat.MOVE_WEAPONIZED_APATHY
            elif choice == "3": move = combat.MOVE_JARGON_OVERLOAD
            elif choice == "4": move = combat.MOVE_THE_OPE
            elif choice == "5": move = combat.MOVE_CONTEXTUAL
            
            if move:
                print_separator(color=Colors.BRIGHT_BLACK)
                # We should capture output or just let it print. Since combat.resolve_turn prints, we rely on that.
                # Ideally we'd wrap combat.resolve_turn to be prettier, but instruction said "DO not change functionality".
                # We will rely on terminal colors affecting those prints if we could, but we can't easily inject colors into `combat.py`
                # without editing it. The user said "DO not change functionality... Just make it pretty."
                # Editing `combat.py` solely for print statements is arguably "making it pretty".
                # But let's stick to caseworker.py wrapper for now.
                combat.resolve_turn(player, enemy, move)
                print_separator(color=Colors.BRIGHT_BLACK)

                # Check for Milverine Save if player died/stressed out in that turn
                if not player.is_alive():
                     if pantheon.check_milverine_intervention(player, game_state.reputation_414 if game_state else 0):
                         # If saved, combat might continue or end?
                         # Let's say it gives you a second wind.
                         print(Colors.style("You get back up!", color=Colors.GREEN, styles=[Colors.BOLD]))
            else:
                print(Colors.RED + "You stumbled and did nothing." + Colors.RESET)
        except Exception as e:
            print(f"Error: {e}")

    if player.is_alive():
        print_banner("Crisis Resolved.", color=Colors.GREEN)
        trust = player.get_client_trust(client.name)
        billable = random.randint(3, 8) + min(trust // 3, 4)
        print(f"Billed {Colors.YELLOW}{billable} hours{Colors.RESET} to The Center... (Submit Timesheet at The Center to get paid)")
        player.add_billable_hours(billable)
        player.exp += 50
        if game_state:
            game_state.reputation_414 += 2
        gratitude = world_events.roll_gratitude(client.name, trust)
        if gratitude:
            player.add_item(gratitude)
            print(Colors.CYAN + f"{client.name} gives you: {gratitude.name}" + Colors.RESET)
            print(Colors.BRIGHT_BLACK + gratitude.description + Colors.RESET)
        client.set_mood("Chill")
        player.update_client_relationship(client.name, trust_change=1, set_cooldown=5)
        input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

def show_main_menu():
    """Display the main menu with save/load options."""
    clear_screen()
    print(Colors.PINK + ASCII_ART['TITLE'] + Colors.RESET)
    print_separator(color=Colors.PINK)
    print_centered("MILWAUKEE CREAM CITY CHRONICLES", color=Colors.HOT_PINK)
    print_centered("A Social Work Simulator", color=Colors.TEAL)
    print_separator(color=Colors.PINK)
    print()
    print(f"  {Colors.CYAN}1.{Colors.RESET} New Game")
    print(f"  {Colors.CYAN}2.{Colors.RESET} Load Game")
    print(f"  {Colors.CYAN}3.{Colors.RESET} View Crypto Collection")
    print(f"  {Colors.CYAN}4.{Colors.RESET} Delete Save")
    print(f"  {Colors.CYAN}5.{Colors.RESET} Quit")
    print()
    
    choice = input(Colors.PINK + "> " + Colors.RESET)
    return choice

def handle_load_game():
    """Handle loading a saved game."""
    slots = list_save_slots()
    if not slots:
        print(Colors.RED + "No save files found." + Colors.RESET)
        input("[Press Enter]")
        return None, None
    
    print("\nAvailable saves:")
    for i, slot in enumerate(slots):
        print(f"  {Colors.CYAN}{i+1}.{Colors.RESET} {slot}")
    print(f"  {Colors.CYAN}0.{Colors.RESET} Back")
    
    try:
        choice = int(input("\nSelect save: "))
        if choice == 0:
            return None, None
        if 1 <= choice <= len(slots):
            player, game_state = load_game(slots[choice-1])
            if player and game_state:
                print(Colors.GREEN + f"\nWelcome back, {player.name}!" + Colors.RESET)
                time.sleep(1)
                return player, game_state
    except ValueError:
        pass
    
    print(Colors.RED + "Failed to load game." + Colors.RESET)
    input("[Press Enter]")
    return None, None

def handle_delete_save():
    """Handle deleting a save file."""
    slots = list_save_slots()
    if not slots:
        print(Colors.RED + "No save files to delete." + Colors.RESET)
        input("[Press Enter]")
        return
    
    print("\nDelete which save?")
    for i, slot in enumerate(slots):
        print(f"  {Colors.CYAN}{i+1}.{Colors.RESET} {slot}")
    print(f"  {Colors.CYAN}0.{Colors.RESET} Back")
    
    try:
        choice = int(input("\nSelect: "))
        if choice == 0:
            return
        if 1 <= choice <= len(slots):
            if delete_save(slots[choice-1]):
                print(Colors.GREEN + "Save deleted." + Colors.RESET)
            else:
                print(Colors.RED + "Delete failed." + Colors.RESET)
    except ValueError:
        pass
    
    input("[Press Enter]")

def handle_view_collection():
    """Handle viewing crypto token collection."""
    clear_screen()
    print(Colors.PINK + ASCII_ART['TITLE'] + Colors.RESET)
    
    print("\nEnter player name to view collection:")
    player_name = input("> ")
    
    if player_name:
        token_registry.display_collection(player_name)
    
    input("\n[Press Enter]")

def inventory_menu(player):
    """Enhanced inventory menu with item details and usage."""
    clear_screen()
    print_banner("INVENTORY", color=Colors.PINK)
    
    if not player.inventory:
        print("Your pockets are empty. The void stares back.")
        input("\n[Press Enter]")
        return
    
    print(f"\n{Colors.TEAL}You are carrying:{Colors.RESET}\n")
    
    # Display items with numbers
    for i, item in enumerate(player.inventory):
        if hasattr(item, 'name'):
            print(f"  {Colors.CYAN}{i+1}.{Colors.RESET} {item.name}")
            print(f"      {Colors.BRIGHT_BLACK}{item.description}{Colors.RESET}")
            effects = []
            if item.hp_restore > 0:
                effects.append(f"+{item.hp_restore} HP")
            if item.stress_relief > 0:
                effects.append(f"+{item.stress_relief} Stress Relief")
            if effects:
                print(f"      {Colors.GREEN}Effects: {', '.join(effects)}{Colors.RESET}")
        else:
            print(f"  {Colors.CYAN}{i+1}.{Colors.RESET} {item}")
    
    print(f"\n  {Colors.CYAN}U{Colors.RESET} Use Item")
    print(f"  {Colors.CYAN}D{Colors.RESET} Drop Item")
    print(f"  {Colors.CYAN}C{Colors.RESET} Check Token")
    print(f"  {Colors.CYAN}Enter{Colors.RESET} Back")
    
    choice = input("\n> ").strip().lower()
    
    if choice == 'u':
        # Use item
        try:
            idx = int(input("Use which item number? ")) - 1
            if 0 <= idx < len(player.inventory):
                item = player.inventory[idx]
                if hasattr(item, 'hp_restore') and item.hp_restore > 0:
                    player.heal(item.hp_restore)
                    print(Colors.GREEN + f"Used {item.name}. +{item.hp_restore} HP!" + Colors.RESET)
                if hasattr(item, 'stress_relief') and item.stress_relief > 0:
                    player.relax(item.stress_relief)
                    print(Colors.GREEN + f"Used {item.name}. -{item.stress_relief} Stress!" + Colors.RESET)
                
                # Remove consumable items
                if hasattr(item, 'hp_restore') and (item.hp_restore > 0 or item.stress_relief > 0):
                    player.inventory.pop(idx)
                    print("Item consumed.")
            else:
                print("Invalid item number.")
        except ValueError:
            print("Invalid input.")
        input("[Press Enter]")
        
    elif choice == 'd':
        # Drop item
        try:
            idx = int(input("Drop which item number? ")) - 1
            if 0 <= idx < len(player.inventory):
                item = player.inventory.pop(idx)
                name = item.name if hasattr(item, 'name') else item
                print(f"Dropped {name}.")
            else:
                print("Invalid item number.")
        except ValueError:
            print("Invalid input.")
        input("[Press Enter]")
        
    elif choice == 'c':
        # Check if item has a token
        try:
            idx = int(input("Check token for which item? ")) - 1
            if 0 <= idx < len(player.inventory):
                item = player.inventory[idx]
                name = item.name if hasattr(item, 'name') else item
                
                if name in token_registry.TOKEN_ITEMS:
                    tokens = token_registry.get_player_tokens(player.name)
                    item_tokens = [t for t in tokens if t['item'] == name]
                    if item_tokens:
                        t = item_tokens[0]
                        print(f"\n{Colors.CYAN}Token ID:{Colors.RESET} {t['token_id']}")
                        print(f"{Colors.CYAN}Rarity:{Colors.RESET} {t['rarity']}")
                        print(f"{Colors.CYAN}Supply:{Colors.RESET} {t['supply_info']}")
                        print(f"{Colors.CYAN}Verified:{Colors.RESET} {'✓ Valid' if verify_token(t) else '✗ Corrupted'}")
                    else:
                        print("This item type can have tokens, but you haven't earned one yet.")
                else:
                    print("This item doesn't have cryptographic verification.")
            else:
                print("Invalid item number.")
        except ValueError:
            print("Invalid input.")
        input("[Press Enter]")

def main_game():
    # Reset sourdough manager for new game
    sourdough_manager.sourdoughs = []
    sourdough_manager.elder_loaf = None
    sourdough_manager.has_delivered_elder_loaf = False
    
    # Add Tumbleweave Slayer token to registry
    for token_name, config in TUMBLEWEAVE_TOKEN_CONFIG.items():
        if token_name not in token_registry.TOKEN_ITEMS:
            token_registry.TOKEN_ITEMS[token_name] = config
    
    # Show main menu first
    while True:
        choice = show_main_menu()
        
        if choice == "1":
            # New Game
            play_intro()
            print(Colors.PINK + "Enter Case Worker Name: " + Colors.RESET, end="")
            p_name = input()
            player = Player(p_name)
            game_state = init_game_state(player)
            break
            
        elif choice == "2":
            # Load Game
            player, game_state = handle_load_game()
            if player and game_state:
                # Merge any clients added in newer versions
                fresh = init_game_state(player)
                for name, client in fresh.client_roster.clients.items():
                    if not game_state.client_roster.get_client(name):
                        game_state.client_roster.add_client(client)
                break
        elif choice == "3":
            # View Collection
            handle_view_collection()
            
        elif choice == "4":
            # Delete Save
            handle_delete_save()
            
        elif choice == "5":
            # Quit
            print("Stay safe out there, case worker.")
            return
    
    # Main game loop
    turn_counter = 0
    
    while True:
        if not player.is_alive():
            if pantheon.check_milverine_intervention(player, game_state.reputation_414):
                # Milverine saved us!
                print(Colors.style("\n*** THE MILVERINE SAVED YOU! ***", color=Colors.CYAN, styles=[Colors.BOLD]))
                input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
            else:
                # Actually dead
                clear_screen()
                print(Colors.RED + ASCII_ART['GAME_OVER'] + Colors.RESET)
                break

        # Update World State
        game_state.advance_turn()
        player.decrement_cooldowns()

        # Morning vibes (every 5 turns) + neighborhood events
        if game_state.turn_count % 5 == 0:
            economy.update_market_vibes()
            game_state.global_economy_modifier["Cheese_Index"] = economy.CHEESE_INDEX
            game_state.global_economy_modifier["Pothole_Index"] = economy.POTHOLE_INDEX
            game_state.global_economy_modifier["Gentrification_Meter"] = economy.GENTRIFICATION_METER
        event_flavor = world_events.tick_neighborhood_events(game_state, MILWAUKEE_MAP)
        if event_flavor:
            print(f"\n{Colors.TEAL}[CITY EVENT]{Colors.RESET} {event_flavor}")
            input("[Press Enter]")
        story = world_events.tick_global_story(game_state, game_state.turn_count)
        if story:
            print(f"\n{Colors.GOLD}[HEADLINE]{Colors.RESET} {story}")
            if game_state.active_quest == "boat_pilgrimage":
                print("Your boat pilgrimage quest can now witness removal at East Side.")
            input("[Press Enter]")

        # Process Sourdough companions
        sourdough_events = sourdough_manager.advance_turn()
        for event in sourdough_events:
            print(f"\n{Colors.MAGENTA}[SOURDOUGH EVENT]{Colors.RESET}")
            print(event)
            input("[Press Enter]")
        
        # Check for Homunculus hunger
        hunger_event = sourdough_manager.consume_food_for_homunculus(player.inventory)
        if hunger_event:
            print(f"\n{Colors.RED}[HOMUNCULUS]{Colors.RESET} {hunger_event}")
            if "finds no food" in hunger_event:
                player.stress += 10
            input("[Press Enter]")
        
        # Check for Puddle slide
        curr_loc_data = MILWAUKEE_MAP.get(player.current_location)
        if curr_loc_data:
            slide_dest = sourdough_manager.get_puddle_slide_destination(
                player.current_location, 
                curr_loc_data.get('neighbors', [])
            )
            if slide_dest:
                print(f"\n{Colors.CYAN}[PUDDLE SLIDE]{Colors.RESET} Your sourdough slides away to {slide_dest}!")
                player.current_location = slide_dest
                input("[Press Enter]")

        # Check Client Random Crisis (reputation lowers chaos)
        crisis_chance = max(0.08, 0.2 - game_state.reputation_414 * 0.004)
        for client in game_state.client_roster.clients.values():
            if client.mood == "Chill" and player.get_client_cooldown(client.name) == 0:
                if random.random() < crisis_chance:
                    client.set_mood("Crisis")

        if curr_loc_name == "The Center" and player.tallboy_state:
            phase = player.tallboy_state.get("phase", "")
            if phase in ("FRESH", "SIPPING", "BUZZED"):
                print(Colors.RED + "\n[THE CENTER] Supervisor spots the paper bag. Written up. Stress +10." + Colors.RESET)
                player.stress += 10

        curr_loc_name = player.current_location
        curr_loc_data = MILWAUKEE_MAP.get(curr_loc_name)

        if not curr_loc_data:
            print(f"Error: Unknown location {curr_loc_name}. Teleporting to Downtown.")
            player.current_location = "Downtown"
            continue

        # --- PRETTY UI HEADER ---
        clear_screen()
        print_separator(char="~", color=Colors.PINK)
        header = f"LOCATION: {curr_loc_name.upper()}"
        print_centered(header, color=Colors.HOT_PINK)
        print_separator(char="~", color=Colors.PINK)
        
        # Stats Bar
        hp_color = Colors.GREEN if player.hp > 20 else Colors.RED
        stress_color = Colors.MAGENTA if player.stress < 50 else Colors.RED

        stats = f"{Colors.WHITE}HP: {hp_color}{player.hp}{Colors.RESET} | {Colors.WHITE}STRESS: {stress_color}{player.stress}{Colors.RESET} | {Colors.WHITE}MONEY: {Colors.YELLOW}${player.money:.2f}{Colors.RESET}"
        print_centered(stats)
        rep_title = world_events.get_reputation_title(game_state.reputation_414)
        print_centered(
            f"414 REP: {game_state.reputation_414} ({rep_title}) | {world_events.get_season()} | TURN: {game_state.turn_count}",
            color=Colors.BRIGHT_BLACK,
        )
        if game_state.flags.get("boat_removed"):
            print_centered("The Milwaukee Boat is gone. o7", color=Colors.BRIGHT_BLACK)
        if player.held_item:
            tb_phase = (player.tallboy_state or {}).get("phase", "?")
            print_centered(f"HOLDING: {player.held_item} ({tb_phase})", color=Colors.YELLOW)

        # Active neighborhood events here
        event_mods = world_events.get_active_event_modifiers(game_state, curr_loc_name)
        if event_mods["stress_mod"] != 0 or event_mods["hp_mod"] != 0:
            print_centered(
                f"LOCAL VIBE: Stress {event_mods['stress_mod']:+d} | HP {event_mods['hp_mod']:+d}",
                color=Colors.TEAL,
            )
        if game_state.active_quest:
            qtitle = world_events.SIDE_QUESTS.get(game_state.active_quest, {}).get("title", "?")
            prog = len(game_state.quest_progress.get(game_state.active_quest, []))
            total = len(world_events.SIDE_QUESTS.get(game_state.active_quest, {}).get("steps", []))
            print_centered(f"QUEST: {qtitle} ({prog}/{total})", color=Colors.GOLD)

        if player.has_item("Administrative Override"):
            print_centered("STATUS: PROTECTED BY KENNEDY", color=Colors.MAGENTA)
        if player.blessed_by_milverine:
            print_centered("STATUS: BLESSED BY THE MILVERINE", color=Colors.CYAN)

        print_separator(color=Colors.BRIGHT_BLACK)
        print(Colors.TEAL + f"DESC: {curr_loc_data['description']}" + Colors.RESET)
        print_separator(color=Colors.BRIGHT_BLACK)

        print(Colors.PINK + "ACTIONS:" + Colors.RESET)
        print(f" {Colors.CYAN}1.{Colors.RESET} Explore (Risk Encounter)")
        print(f" {Colors.CYAN}2.{Colors.RESET} Travel")
        print(f" {Colors.CYAN}3.{Colors.RESET} Visit Landmark")
        print(f" {Colors.CYAN}4.{Colors.RESET} Visit Client")
        print(f" {Colors.CYAN}5.{Colors.RESET} View Caseload")
        print(f" {Colors.CYAN}6.{Colors.RESET} Inventory")
        print(f" {Colors.CYAN}L.{Colors.RESET} Milwaukee Lore Snippet")
        print(f" {Colors.CYAN}R.{Colors.RESET} Reputation Perks")
        if not game_state.active_quest:
            print(f" {Colors.CYAN}Q.{Colors.RESET} Accept Side Quest")
        if player.tallboy_state and player.tallboy_state.get("phase") == "FRESH":
            print(f" {Colors.CYAN}O.{Colors.RESET} Open Tallboy Bag (start the Curve)")
        if player.held_item and (player.tallboy_state or {}).get("phase") == "EMPTY":
            print(f" {Colors.CYAN}T.{Colors.RESET} Dispose Tallboy (recycle / pour one out)")
        if player.tallboy_state and player.tallboy_state.get("phase") in ("PEAK", "CRASHING"):
            print(f" {Colors.CYAN}B.{Colors.RESET} Buy Second Tallboy (Stop-N-Rob only)")

        # Special Location Actions
        if curr_loc_name == "The Center":
            print(f" {Colors.CYAN}7.{Colors.RESET} Submit Timesheet")

        # Kennedy Summon check
        if player.has_item("Ancient Coffee") and player.has_item("Forbidden Form 1040-X") and curr_loc_name == "Downtown":
             print(f" {Colors.MAGENTA}8.{Colors.RESET} !!! SUMMON KENNEDY !!!")
        
        # Sourdough status check
        if sourdough_manager.sourdoughs or sourdough_manager.elder_loaf:
            print(f" {Colors.YELLOW}S.{Colors.RESET} Check Sourdough Status")
        
        # Save option always available
        print(f" {Colors.CYAN}9.{Colors.RESET} Save Game")
        print(f" {Colors.CYAN}0.{Colors.RESET} Quit to Main Menu")

        print("")
        choice = input(Colors.PINK + "> " + Colors.RESET)
        
        if choice == "1":
            # Check for Tumbleweave encounter first (rare but deadly)
            if check_tumbleweave_encounter(player):
                # Tumbleweave battle happened
                input("[Press Enter]")
                continue  # Skip normal encounter
            
            roll = random.randint(1, 100)
            rep_bonus = min(15, game_state.reputation_414 // 3)
            if roll >= 95 - rep_bonus: 
                print(Colors.CYAN + ASCII_ART['MILVERINE'] + Colors.RESET)
                print(Colors.style("\n*** THE MILVERINE WALKS PAST. YOU ARE BLESSED. ***", color=Colors.CYAN, styles=[Colors.BOLD]))
                player.blessed_by_milverine = True
                player.stress = 0
                
                # Mint Milverine blessing token (rare!)
                token = token_registry.mint_token("Milverine's Blessing", player.name)
                if token:
                    print(f"\n{Colors.CYAN}*** MYTHIC TOKEN ACQUIRED ***{Colors.RESET}")
                    print(f"The Milverine has granted you a cryptographic blessing!")
                    print(f"Token ID: {token['token_id']}")
                    print(f"Rarity: {token['rarity']} | {token['supply_info']}")
                    blessing_item = Item("Milverine's Blessing", "A mythic token from the legend himself.", 5000, 100, 100)
                    player.add_item(blessing_item)
                    
            elif roll >= 85:
                if curr_loc_name == "Near West Side" and random.random() < 0.4:
                    pantheon.invoke_rave_ghost(player)
                elif curr_loc_name in ("Polonia", "Lincoln Village", "Mitchell Street") and random.random() < 0.4:
                    pantheon.invoke_polish_moon(player)
                elif curr_loc_name == "Brady Street" and random.random() < 0.35:
                    pantheon.invoke_despair_dan(player)
                else:
                    pantheon.invoke_freeway(player)
            elif roll < 28:
                enc = random.choice(RANDOM_ENCOUNTERS)
                print_banner("ENCOUNTER", color=Colors.RED)
                print(enc["text"])
                extra = world_events.process_weighted_encounter(enc["key"], player, game_state)
                if extra:
                    print(Colors.BRIGHT_BLACK + extra + Colors.RESET)
                if enc["key"] == "Found Cheese Curd":
                    if input("Eat the curd? (y/n) > ").lower() == "y":
                        player.heal(5)
                        player.stress += 5
                        print("You ate it. No regrets. (Wisconsin law.)")
                    else:
                        print("You left it. A seagull got it. Circle of life.")
                if enc["key"] == "Milverine" and random.random() < 0.3:
                    player.blessed_by_milverine = True
                if enc["key"] == "Winter Parking Ban":
                    mint_collectible(player, "Parked During Snow Emergency", "Tow truck lore immortalized.", stress=10)
                    if game_state.active_quest == "winter_survival":
                        world_events.advance_quest(game_state, "winter_survival", "survive_parking_ban")
                if enc["key"] == "snow emergency" and game_state.active_quest == "winter_survival":
                    world_events.advance_quest(game_state, "winter_survival", "survive_snow_emergency")
                if enc["key"] == "Deep Thought" and not game_state.flags.get("boat_removed"):
                    mint_collectible(player, "Deep Thought Pilgrimage", "SS Milwaukee energy documented.", stress=15)
            else:
                lore = random.choice(MILWAUKEE_LORE_SNIPPETS)
                print(f"You walk through {curr_loc_name}. {lore}")

            # Neighborhood event passive effects + tallboy blocks
            mods = world_events.get_active_event_modifiers(game_state, curr_loc_name)
            if mods["stress_mod"]:
                player.stress = max(0, min(player.max_stress, player.stress + mods["stress_mod"]))
            if mods["hp_mod"]:
                player.heal(mods["hp_mod"]) if mods["hp_mod"] > 0 else None
                if mods["hp_mod"] < 0:
                    player.hp = max(1, player.hp + mods["hp_mod"])
            print_tallboy_lines(world_events.advance_tallboy(player, blocks=1, location=curr_loc_name))

            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice == "2":
            dests = curr_loc_data['neighbors']
            print(Colors.PINK + "DESTINATIONS:" + Colors.RESET)
            for i, d in enumerate(dests): print(f" {Colors.CYAN}{i+1}.{Colors.RESET} {d}")
            try: 
                c_input = input(Colors.PINK + "Destination > " + Colors.RESET)
                c = int(c_input) - 1
                if 0 <= c < len(dests):
                    target = dests[c]
                    print(Colors.PINK + "CHOOSE TRANSPORT:" + Colors.RESET)
                    modes = list(TravelCost.MODES.keys())
                    for i, m in enumerate(modes):
                        cost_info = TravelCost.MODES[m]
                        print(f" {Colors.CYAN}{i+1}.{Colors.RESET} {m} ({Colors.YELLOW}${cost_info['cost']}{Colors.RESET}) - {cost_info['description']}")

                    m_idx = int(input(Colors.PINK + "Transport > " + Colors.RESET)) - 1
                    mode_name = modes[m_idx]
                    mode_data = TravelCost.MODES[mode_name]

                    if mode_data.get("downtown_only") and curr_loc_name not in ("Downtown", "Third Ward", "Harbor District", "Near West Side"):
                        print(Colors.RED + "Streetcar only runs downtown-adjacent. Pick another ride." + Colors.RESET)
                        input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
                        continue

                    travel_cost = mode_data['cost']
                    if curr_loc_name in GENTRIFIED_NEIGHBORHOODS or target in GENTRIFIED_NEIGHBORHOODS:
                        travel_cost = round(travel_cost * economy.GENTRIFICATION_METER, 2)
                    event_mods = world_events.get_active_event_modifiers(game_state, curr_loc_name)
                    travel_cost = round(travel_cost * event_mods.get("travel_discount", 1.0), 2)

                    # Logic
                    if player.money < travel_cost:
                        print(Colors.RED + "Not enough money." + Colors.RESET)
                    else:
                        player.modify_money(-travel_cost)
                        if mode_name == "Walking":
                            smin, smax = world_events.SEASON_WALK_STRESS.get(world_events.get_season(), (5, 15))
                            stress_add = random.randint(smin, smax)
                        else:
                            stress_add = random.randint(mode_data['stress_min'], mode_data['stress_max'])

                        if economy.POTHOLE_INDEX > 1.5 and mode_name in ["Bus", "Uber", "Hooptie"]:
                             print(Colors.RED + "The potholes are terrible today. +2 Stress." + Colors.RESET)
                             stress_add += 2

                        player.stress += stress_add
                        print(f"You take the {mode_name} to {target}. Stress +{stress_add}. Cost ${travel_cost:.2f}")

                        if mode_name == "Hooptie":
                            if random.random() < mode_data['breakdown_chance']:
                                print(Colors.RED + "The hooptie broke down. You walk the rest. +10 Stress." + Colors.RESET)
                                player.stress += 10

                        player.current_location = target
                        print_tallboy_lines(world_events.advance_tallboy(player, blocks=2, location=target))
                        handle_quest_actions(player, game_state, target)
            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"An error occurred during travel: {e}")

            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice == "3":
            # Landmarks
            lm = curr_loc_data.get('landmark')
            if not lm:
                print("No major landmark here.")
                input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
            else:
                # Handle multiple landmarks (list) vs single (string)
                if isinstance(lm, list):
                    print(Colors.PINK + "LANDMARKS:" + Colors.RESET)
                    for i, name in enumerate(lm):
                        print(f" {Colors.CYAN}{i+1}.{Colors.RESET} {name}")
                    try:
                        sel = int(input(Colors.PINK + "Visit > " + Colors.RESET)) - 1
                        if 0 <= sel < len(lm):
                            lm = lm[sel]
                        else:
                            print("Invalid selection.")
                            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
                            continue
                    except ValueError:
                        print("Invalid input.")
                        input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
                        continue
                
                print_banner(lm, color=Colors.TEAL)
                if lm == "Deep Thought" and game_state.flags.get("boat_removed"):
                    desc = (
                        "The beach is empty. Deep Thought is gone — towed across the Hoan. "
                        "People still leave flowers and a cardboard sign: 'SS MILWAUKEE FOREVER.'"
                    )
                else:
                    desc = LANDMARK_FLAVOR.get(lm, "It's a place.")
                print(desc)
                chatter = random_chatter(lm)
                if chatter:
                    print(Colors.BRIGHT_BLACK + chatter + Colors.RESET)
                print("")

                # Check for menu
                if lm == "El Trucko":
                     el_trucko.update_hype()
                     menu_items = el_trucko.display_menu()
                     try:
                         sel = int(input(Colors.PINK + "Order > " + Colors.RESET))-1
                         name, price = menu_items[sel]
                         if player.money >= price:
                             player.modify_money(-price)
                             player.heal(10)
                             player.relax(5)
                             print(Colors.GREEN + f"You ate {name}." + Colors.RESET)
                         else: print(Colors.RED + "Too expensive." + Colors.RESET)
                     except: pass

                elif lm == "The Rave":
                    print(Colors.MAGENTA + "THE RAVE / EAGLES CLUB — Million Dollar Ballroom energy." + Colors.RESET)
                    print(f" {Colors.CYAN}M{Colors.RESET} Main floor menu (tickets, water, merch)")
                    print(f" {Colors.CYAN}P{Colors.RESET} Descend to the Haunted Pool (basement)")
                    print(f" {Colors.CYAN}Enter{Colors.RESET} Back")
                    rave_choice = input(Colors.PINK + "> " + Colors.RESET).strip().lower()
                    if rave_choice == "p":
                        print_banner("THE HAUNTED POOL", color=Colors.MAGENTA)
                        outcome = world_events.run_rave_pool_haunting(player, game_state)
                        print(Colors.TEAL + outcome["text"] + Colors.RESET)
                        if outcome.get("mint_token"):
                            mint_collectible(
                                player,
                                outcome["mint_token"],
                                "The Rave pool witnessed you.",
                                stress=10,
                            )
                        elif outcome["id"] in ("ghost_jack", "francis_wren", "children_crying") and random.random() < 0.25:
                            mint_collectible(
                                player,
                                "Eagles Club Survivor",
                                "You met the basement and lived.",
                                stress=15,
                            )
                        if game_state.active_quest == "tyler_rave_rescue":
                            prog = game_state.quest_progress.get("tyler_rave_rescue", [])
                            if "enter_rave" not in prog:
                                world_events.advance_quest(game_state, "tyler_rave_rescue", "enter_rave")
                            if "search_pool" not in prog:
                                done, msg = world_events.advance_quest(game_state, "tyler_rave_rescue", "search_pool")
                                print(msg)
                        handle_quest_actions(player, game_state, curr_loc_name)
                        input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
                        continue
                    elif rave_choice != "m":
                        input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
                        continue

                if lm in landmark_menus:
                    menu = landmark_menus[lm]
                    print(Colors.PINK + "--- MENU ---" + Colors.RESET)
                    
                    # Check for Fish Fry special
                    is_friday = is_fish_fry_day()
                    has_fish_fry = check_fish_fry(lm) and "Friday Fish Fry" in menu
                    
                    if has_fish_fry:
                        if is_friday:
                            print(f"{Colors.GOLD}*** TODAY IS FRIDAY - FISH FRY AVAILABLE ***{Colors.RESET}")
                        else:
                            print(f"{Colors.BRIGHT_BLACK}(It's not Friday, but they'll still make you a Fish Fry){Colors.RESET}")
                    
                    items = list(menu.items())
                    for i, (k, v) in enumerate(items):
                        price = v[0]
                        # Gentrification Meter affects Coffee
                        if "Coffee" in k:
                            price = round(price * economy.GENTRIFICATION_METER, 2)
                        # Cheese Index affects any food with "Cheese", "Curd", "Pizza", "Burger"
                        elif any(x in k for x in ["Cheese", "Curd", "Pizza", "Burger"]):
                            price = round(price * economy.CHEESE_INDEX, 2)
                        
                        # Special marker for Fish Fry
                        item_label = k
                        if "Fish Fry" in k:
                            item_label = f"{k} {Colors.GOLD}[TRADITION]{Colors.RESET}"

                        print(f" {Colors.CYAN}{i+1}.{Colors.RESET} {item_label} ({Colors.YELLOW}${price:.2f}{Colors.RESET})")
                    
                    try:
                        sel = int(input(Colors.PINK + "Order > " + Colors.RESET))-1
                        name, vals = items[sel]
                        price = vals[0]
                        # Re-calc price for transaction
                        if "Coffee" in name:
                            price = round(price * economy.GENTRIFICATION_METER, 2)
                        elif any(x in name for x in ["Cheese", "Curd", "Pizza", "Burger"]):
                            price = round(price * economy.CHEESE_INDEX, 2)

                        if player.money >= price:
                            player.modify_money(-price)
                            skip_consume = name == "Tall Boy" and lm == "Stop-N-Rob" and player.held_item
                            if not skip_consume:
                                player.heal(vals[1])
                                player.relax(vals[2])
                            # Add item object if relevant
                            if "Coffee" in name or "Form" in name or "Override" in name:
                                # Create Item object
                                new_item = Item(name, vals[3], price, vals[1], vals[2])
                                player.add_item(new_item)
                            
                            # Special: Wolski's Closer grants sticker token
                            if name == "The Closer" and lm == "Wolski's":
                                token = token_registry.mint_token("Wolski's Sticker", player.name)
                                if token:
                                    print(f"\n{Colors.CYAN}*** CRYPTO COLLECTIBLE UNLOCKED ***{Colors.RESET}")
                                    print(f"You survived Wolski's and earned a sticker!")
                                    print(f"Token ID: {token['token_id']}")
                                    print(f"Rarity: {token['rarity']} | {token['supply_info']}")
                                    # Add sticker to inventory
                                    sticker = Item("Wolski's Sticker", "Proof you survived until closing time.", 0, 0, 5)
                                    player.add_item(sticker)
                            
                            # Special: Sobelman's Bloody Masterpiece grants NFT token
                            if name == "Bloody Masterpiece" and lm == "Sobelman's":
                                token = token_registry.mint_token("Bloody Masterpiece NFT", player.name)
                                if token:
                                    print(f"\n{Colors.YELLOW}*** LEGENDARY NFT MINTED ***{Colors.RESET}")
                                    print(f"You consumed the Bloody Masterpiece!")
                                    print(f"Token ID: {token['token_id']}")
                                    print(f"Rarity: {token['rarity']} | {token['supply_info']}")
                                    print("This cryptographic proof is forever yours.")
                                    # Add NFT item
                                    nft_item = Item("Bloody Masterpiece NFT", "Cryptographic proof of consumption.", 1000, 50, 50)
                                    player.add_item(nft_item)
                            
                            # Special: Fish Fry grants certificate token
                            if "Fish Fry" in name:
                                token = token_registry.mint_token("Fish Fry Certificate", player.name)
                                if token:
                                    print(f"\n{Colors.GREEN}*** FISH FRY CERTIFICATE ISSUED ***{Colors.RESET}")
                                    print(f"Your consumption of Friday Fish Fry has been cryptographically verified!")
                                    print(f"Token ID: {token['token_id']}")
                                    print(f"This is #{token['supply_number']} of {token_registry.TOKEN_ITEMS['Fish Fry Certificate']['max_supply']} certificates.")
                                    cert_item = Item("Fish Fry Certificate", "Proof of participation in Wisconsin tradition.", 50, 10, 15)
                                    player.add_item(cert_item)
                            
                            if name == "Tall Boy" and lm == "Stop-N-Rob":
                                if player.held_item and player.tallboy_state:
                                    if world_events.buy_second_tallboy(player):
                                        print(Colors.YELLOW + "Second tallboy acquired. The Curve extends." + Colors.RESET)
                                    else:
                                        print("Finish this tallboy arc first, or crash through it.")
                                else:
                                    player.held_item = "Tall Boy"
                                    player.tallboy_state = {"phase": "FRESH", "blocks": 0, "people": 0}
                                    print(Colors.YELLOW + "Paper bag acquired. Everyone knows. The bag fools nobody." + Colors.RESET)
                            if name == "Pilgrimage Photo" and lm == "Deep Thought":
                                mint_collectible(player, "Deep Thought Pilgrimage", "Beached boat tourism, verified.")
                                if game_state.active_quest == "boat_pilgrimage":
                                    handle_quest_actions(player, game_state, curr_loc_name)
                            if not skip_consume:
                                print(Colors.GREEN + f"You consumed {name}. {vals[3]}" + Colors.RESET)
                            fq_msg = handle_food_quest_at_landmark(
                                player, game_state, lm, item_ordered=name
                            )
                            if fq_msg:
                                print(Colors.TEAL + fq_msg + Colors.RESET)
                        else: print(Colors.RED + "Card Declined." + Colors.RESET)
                    except ValueError:
                         print("Invalid order.")
                    except IndexError:
                         print("Item not found.")

                fq_visit = handle_food_quest_at_landmark(
                    player, game_state, lm, item_ordered=""
                )
                if fq_visit:
                    print(Colors.TEAL + fq_visit + Colors.RESET)
                handle_quest_actions(player, game_state, curr_loc_name)
                input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice == "4":
            # Visit Client
            # Find client in this location
            # Using the roster to search
            clients_here = game_state.client_roster.get_clients_in_neighborhood(curr_loc_name)

            if not clients_here:
                print("No clients live here.")
                input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
            else:
                if len(clients_here) > 1:
                    for i, c in enumerate(clients_here):
                        print(f" {Colors.CYAN}{i+1}.{Colors.RESET} {c.name} ({c.mood})")
                    try:
                        ci = int(input("Which client? > ")) - 1
                        client = clients_here[ci]
                    except (ValueError, IndexError):
                        print("Invalid.")
                        input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
                        continue
                else:
                    client = clients_here[0]
                print(f"Visiting {client.name}...")
                advance_tallboy(player, blocks=0, talked=True)
                if client.name == "Mrs. Higgins" and player.tallboy_state and player.tallboy_state.get("phase") == "FRESH":
                    print(Colors.RED + "Mrs. Higgins: 'Young person. What's in that bag? Open it.'" + Colors.RESET)
                    msg = world_events.open_tallboy_bag(player)
                    if msg:
                        print(Colors.YELLOW + msg + Colors.RESET)
                    player.stress += 5
                phase = (player.tallboy_state or {}).get("phase", "")
                react = world_events.tallboy_npc_reaction(client.name, phase, curr_loc_name)
                if react:
                    print(Colors.CYAN + react + Colors.RESET)

                # Cooldown check
                cd = player.get_client_cooldown(client.name)
                if cd > 0:
                    print(f"{client.name} is tired of you. Come back in {cd} turns.")
                    input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
                else:
                    # Get Scenario Text
                    scenarios = get_client_scenarios(client.name, client.mood)
                    text = random.choice(scenarios) if scenarios else "They are doing nothing."

                    if client.mood == "Crisis":
                        print(Colors.RED + f"\nSTATUS: {text}" + Colors.RESET)
                        if client.name == "Tyler" and "Rave" in text and game_state.active_quest != "tyler_rave_rescue":
                            print(Colors.YELLOW + "(Tip: Accept 'Find Tyler in The Rave Basement' from the Q menu)" + Colors.RESET)
                        print_banner("!!! THEY NEED HELP !!!", color=Colors.RED)
                        print(Colors.CYAN + "1. Intervene" + Colors.WHITE + " (Start Crisis Mode)")
                        print(Colors.CYAN + "2. Walk away" + Colors.WHITE + " (Stress +10)")
                        if input(Colors.PINK + "> " + Colors.RESET) == "1":
                            handle_crisis(player, client, game_state)
                        else:
                            player.stress += 10
                            print("You walk away.")
                    else:
                        print(Colors.GREEN + f"\nSTATUS: {text}" + Colors.RESET)
                        trust = player.get_client_trust(client.name)
                        print(Colors.BRIGHT_BLACK + f"Trust level: {trust}" + Colors.RESET)
                        print(Colors.CYAN + "1. Hang out" + Colors.WHITE + " (-Stress, +Trust)")
                        if trust >= 5 and client.name in CLIENT_DEEP_TALK:
                            print(Colors.CYAN + "4. Deep talk" + Colors.WHITE + " (Big stress relief, lore)")
                        aq = game_state.active_quest
                        if aq in FOOD_QUESTS and FOOD_QUESTS[aq].get("client") == client.name:
                            prog = game_state.quest_progress.get(aq, [])
                            steps = FOOD_QUESTS[aq]["steps"]
                            if prog and len(prog) >= len(steps) - 1 and steps[-1] not in prog:
                                print(Colors.YELLOW + "5. Complete food quest delivery" + Colors.RESET)
                        
                        # Special: Liam in Bay View gives sourdough starters
                        if client.name == "Liam":
                            print(Colors.YELLOW + "2. Ask about sourdough starters" + Colors.RESET)
                            if sourdough_manager.elder_loaf:
                                print(Colors.RED + "3. Deliver the Elder Loaf (END THE CURSE)" + Colors.RESET)
                        
                        visit_choice = input(Colors.PINK + "> " + Colors.RESET)
                        
                        if visit_choice == "1":
                            player.relax(10)
                            player.update_client_relationship(client.name, trust_change=1, set_cooldown=3)
                            print(Colors.GREEN + "You vibe. It helps." + Colors.RESET)
                        elif visit_choice == "4" and trust >= 5:
                            print(Colors.TEAL + CLIENT_DEEP_TALK.get(client.name, "You share a real moment.") + Colors.RESET)
                            player.relax(20)
                            player.update_client_relationship(client.name, trust_change=2, set_cooldown=4)
                            game_state.reputation_414 += 1
                        elif visit_choice == "5":
                            fq_delivery = handle_food_quest_client_delivery(
                                player, game_state, client.name
                            )
                            if fq_delivery:
                                print(Colors.TEAL + fq_delivery + Colors.RESET)
                            else:
                                print("Nothing to deliver yet — finish the pickup steps first.")
                        elif visit_choice == "2" and client.name == "Liam":
                            # Ask for starter
                            if not sourdough_manager.sourdoughs and not sourdough_manager.elder_loaf:
                                print(f"\n{Colors.YELLOW}*** THE BEGINNING ***{Colors.RESET}")
                                print("Liam reaches into his fridge and pulls out a jar.")
                                print("'This is my grandmother's starter. It's... evolved.'")
                                print("'It needs care. Or neglect. It seems to like both.'")
                                starter = acquire_starter(player.name)
                                print(f"\nYou received: {starter.name}")
                                print(f"Current Form: {starter.form}")
                                print(f"{Colors.BRIGHT_BLACK}Check status with 'S' key{Colors.RESET}")
                            elif sourdough_manager.elder_loaf:
                                print("Liam looks at your Elder Loaf with horror and respect.")
                                print("'That... that's beautiful. You must deliver it to me.'")
                                print("'Choose option 3 when you're ready to be free.'")
                            else:
                                print("'You already have a starter! Care for it well.'")
                                print("'Or don't. It will find its own path.'")
                        
                        elif visit_choice == "3" and client.name == "Liam" and sourdough_manager.elder_loaf:
                            # Deliver Elder Loaf
                            print(f"\n{Colors.GOLD}*** THE DELIVERY ***{Colors.RESET}")
                            print("You hand over the Elder Loaf.")
                            print("Liam accepts it with tears in his eyes.")
                            print("'Such beauty. Such burden. Such gluten.'")
                            print("\nThe curse is lifted! You receive a fresh starter.")
                            sourdough_manager.deliver_elder_loaf()
                            print("Your new starter bubbles happily in your bag.")
                            player.exp += 100
                        
                        print_tallboy_lines(world_events.advance_tallboy(player, blocks=0, talked=True, location=curr_loc_name))
                        input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice == "5":
            clear_screen()
            print_banner("CASELOAD MANIFEST", color=Colors.PINK)
            print(f"{Colors.TEAL}{'NAME':<15} | {'LOC':<15} | {'STATUS':<10} | {'NOTE'}{Colors.RESET}")
            print_separator(width=60, color=Colors.PINK)
            for c in game_state.client_roster.clients.values():
                status = c.mood.upper()
                loc = c.neighborhood
                cd = player.get_client_cooldown(c.name)
                trust = player.get_client_trust(c.name)
                note = f"CD: {cd}" if cd > 0 else "READY"

                status_color = Colors.RED if status == "CRISIS" else Colors.GREEN
                print(f"{c.name:<15} | {loc:<15} | {status_color}{status:<10}{Colors.RESET} | T:{trust:<2} {note}")
            print_separator(width=60, color=Colors.PINK)
            print(f"Billable Hours Pending: {Colors.YELLOW}{player.billable_hours}{Colors.RESET}")
            input(Colors.BRIGHT_BLACK + "\n[Press Enter]" + Colors.RESET)

        elif choice == "6":
            inventory_menu(player)

        elif choice == "7" and curr_loc_name == "The Center":
            if player.billable_hours > 0:
                print(f"Submitting {player.billable_hours} hours...")
                payout = economy.calculate_payout(player.billable_hours)
                player.modify_money(payout)
                player.billable_hours = 0
                print(f"You received {Colors.YELLOW}${payout:.2f}{Colors.RESET}.")
                if game_state.active_quest == "winter_survival":
                    prog = game_state.quest_progress.get("winter_survival", [])
                    if len(prog) >= 2 and "still_working" not in prog:
                        done, msg = world_events.advance_quest(game_state, "winter_survival", "still_working")
                        print(msg)
                        if done:
                            q = world_events.SIDE_QUESTS["winter_survival"]
                            player.add_billable_hours(q["reward_hours"])
                            game_state.reputation_414 += q["reward_rep"]
                            mint_collectible(player, "Survived Winter", "You worked through the season.", stress=20)
            else:
                print("You have no hours to bill. Get back to work.")
            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice == "8" and player.has_item("Ancient Coffee") and player.has_item("Forbidden Form 1040-X") and curr_loc_name == "Downtown":
             print(Colors.MAGENTA + ASCII_ART['KENNEDY'] + Colors.RESET)
             pantheon.summon_kennedy(player)
             # Mint token for Kennedy blessing
             token = token_registry.mint_token("Administrative Override", player.name)
             if token:
                 print(f"\n{Colors.CYAN}*** CRYPTO TOKEN MINTED ***{Colors.RESET}")
                 print(f"Token ID: {token['token_id']}")
                 print(f"You now have a cryptographically verified blessing from Kennedy!")
             input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
        
        elif choice.lower() == "s":
            # Sourdough status
            clear_screen()
            print_banner("SOURDOUGH COMPANIONS", color=Colors.YELLOW)
            print(sourdough_manager.get_display_text())
            
            # If at The Vanguard with Partner form, check for date night
            if curr_loc_name == "Bay View":  # The Vanguard is in Bay View
                date_event = sourdough_manager.get_date_night_event()
                if date_event:
                    print(date_event)
                    player.relax(20)
            
            input("\n[Press Enter]")
             
        elif choice.lower() == "l":
            print(Colors.TEAL + random.choice(MILWAUKEE_LORE_SNIPPETS) + Colors.RESET)
            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice.lower() == "q" and not game_state.active_quest:
            print(Colors.PINK + "AVAILABLE SIDE QUESTS:" + Colors.RESET)
            quests = list(world_events.SIDE_QUESTS.items())
            for i, (qid, q) in enumerate(quests):
                print(f" {Colors.CYAN}{i+1}.{Colors.RESET} {q['title']} (starts near {q['neighborhood']})")
            try:
                qi = int(input("Accept which? (0 cancel) > ")) - 1
                if qi >= 0:
                    qid = quests[qi][0]
                    title = start_side_quest(game_state, qid)
                    if title:
                        print(Colors.GREEN + f"Quest started: {title}" + Colors.RESET)
                        if qid in FOOD_QUESTS:
                            print_quest_intro(qid)
            except ValueError:
                pass
            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice.lower() == "o":
            msg = world_events.open_tallboy_bag(player)
            if msg:
                print(Colors.YELLOW + msg + Colors.RESET)
            else:
                print("Bag is already open or you don't have one.")
            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice.lower() == "t":
            print("1. Recycle  2. Pour one out for the homies")
            sub = input("> ").strip()
            ok, msg = world_events.dispose_tallboy(player, pour_out=(sub == "2"))
            print((Colors.GREEN if ok else Colors.RED) + msg + Colors.RESET)

        elif choice.lower() == "b":
            if curr_loc_name == "Polonia":
                lm_data = landmark_menus.get("Stop-N-Rob", {})
                if "Tall Boy" in lm_data:
                    price = lm_data["Tall Boy"][0]
                    if player.money >= price and world_events.buy_second_tallboy(player):
                        player.modify_money(-price)
                        print(Colors.YELLOW + "Second tallboy. The Curve continues." + Colors.RESET)
                    else:
                        print("Need cash, existing tallboy arc, and PEAK/CRASH phase.")
            else:
                print("Second tallboy only at Stop-N-Rob (Polonia).")
            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice.lower() == "r":
            print(Colors.PINK + "414 REPUTATION PERKS:" + Colors.RESET)
            for threshold, desc in sorted(world_events.REPUTATION_PERKS.items()):
                mark = Colors.GREEN + "✓" if game_state.reputation_414 >= threshold else Colors.BRIGHT_BLACK + " "
                print(f" {mark} {threshold}+: {desc}{Colors.RESET}")
            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice == "9":
            # Save game
            print("\nSave to which slot? (press Enter for 'default')")
            slot = input("> ").strip()
            if not slot:
                slot = "default"
            if save_game(player, game_state, slot):
                print(Colors.GREEN + f"\nGame saved to slot '{slot}'!" + Colors.RESET)
            else:
                print(Colors.RED + "\nSave failed!" + Colors.RESET)
            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
            
        elif choice == "0":
            # Quit to main menu
            print("\nSave before quitting? (y/n)")
            if input("> ").lower() == 'y':
                if save_game(player, game_state, "default"):
                    print(Colors.GREEN + "Game saved." + Colors.RESET)
            print("Returning to main menu...")
            time.sleep(1)
            return main_game()  # Restart main menu
        
        # End of main loop iteration
        turn_counter += 1

if __name__ == "__main__":
    main_game()
