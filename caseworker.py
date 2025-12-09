import random
import time
import sys
import pantheon
import economy
import combat
from engine import Player, GameState, Client, Item
from world_data import MILWAUKEE_MAP, TravelCost
from text_assets import CLIENT_SCENARIOS, LANDMARK_FLAVOR, RANDOM_ENCOUNTERS, ASCII_ART
from graphics import Colors, clear_screen, typewriter_print, print_centered, print_banner, print_separator

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
        "Cheese Balls": (9.00, 5, 5, "Grease is a love language.")
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
        "The Closer": (7.00, 0, 20, "You get a sticker that says you survived."),
        "Popcorn": (0.00, 2, 0, "It's free and salty.")
    }
}

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
        "Tyler": "East Side"
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
        return {"name": "The Looming Deadline", "hp": 40, "weakness": "Logic"}
    return {"name": "Generic Bureaucrat", "hp": 50, "weakness": "Paperwork"}

def get_client_scenarios(client_name, mood):
    """
    Returns the list of scenarios for a client based on mood from TEXT_ASSETS.
    """
    scenarios = CLIENT_SCENARIOS.get(client_name, [])
    # Filter by mood (Tuple: (Mood, Text))
    return [s[1] for s in scenarios if s[0] == mood]

# --- GAME LOOP ACTIONS ---

def handle_crisis(player, client):
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
                     if pantheon.check_milverine_intervention(player):
                         # If saved, combat might continue or end?
                         # Let's say it gives you a second wind.
                         print(Colors.style("You get back up!", color=Colors.GREEN, styles=[Colors.BOLD]))
            else:
                print(Colors.RED + "You stumbled and did nothing." + Colors.RESET)
        except Exception as e:
            print(f"Error: {e}")

    if player.is_alive():
        print_banner("Crisis Resolved.", color=Colors.GREEN)
        billable = random.randint(3, 8)
        print(f"Billed {Colors.YELLOW}{billable} hours{Colors.RESET} to The Center... (Submit Timesheet at The Center to get paid)")
        player.add_billable_hours(billable)
        player.exp += 50
        client.set_mood("Chill")
        # Set cooldown
        player.update_client_relationship(client.name, trust_change=1, set_cooldown=5)
        input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

def main_game():
    play_intro()
    print(Colors.PINK + "Enter Case Worker Name: " + Colors.RESET, end="")
    p_name = input()
    player = Player(p_name)
    game_state = init_game_state(player)
    
    while True:
        if not player.is_alive():
            if pantheon.check_milverine_intervention(player):
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

        # Check Client Random Crisis
        for client in game_state.client_roster.clients.values():
            if client.mood == "Chill" and player.get_client_cooldown(client.name) == 0:
                if random.random() < 0.2: # 20% chance
                    client.set_mood("Crisis")

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

        # Special Location Actions
        if curr_loc_name == "The Center":
            print(f" {Colors.CYAN}7.{Colors.RESET} Submit Timesheet")

        # Kennedy Summon check
        if player.has_item("Ancient Coffee") and player.has_item("Forbidden Form 1040-X") and curr_loc_name == "Downtown": # Assuming Library is Downtown
             print(f" {Colors.MAGENTA}8. !!! SUMMON KENNEDY !!!{Colors.RESET}")

        print("")
        choice = input(Colors.PINK + "> " + Colors.RESET)
        
        if choice == "1":
            roll = random.randint(1, 100)
            if roll >= 95: 
                print(Colors.CYAN + ASCII_ART['MILVERINE'] + Colors.RESET)
                print(Colors.style("\n*** THE MILVERINE WALKS PAST. YOU ARE BLESSED. ***", color=Colors.CYAN, styles=[Colors.BOLD]))
                player.blessed_by_milverine = True
                player.stress = 0
            elif roll >= 85:
                pantheon.invoke_freeway(player)
            elif roll < 20:
                encounter = random.choice(RANDOM_ENCOUNTERS)
                print_banner("ENCOUNTER", color=Colors.RED)
                print(encounter)
                if "Kia Boys" in encounter: player.stress += 10
                if "Bridge" in encounter: player.stress += 5
            else:
                print(f"You walk through {curr_loc_name}. Nothing weird happens (yet).")

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

                    # Logic
                    if player.money < mode_data['cost']:
                        print(Colors.RED + "Not enough money." + Colors.RESET)
                    else:
                        player.modify_money(-mode_data['cost'])
                        stress_add = random.randint(mode_data['stress_min'], mode_data['stress_max'])

                        # Apply Global Modifiers
                        economy.update_market_vibes()
                        if economy.POTHOLE_INDEX > 1.5 and mode_name in ["Bus", "Uber", "Hooptie"]:
                             print(Colors.RED + "The potholes are terrible today. +2 Stress." + Colors.RESET)
                             stress_add += 2

                        player.stress += stress_add
                        print(f"You take the {mode_name}. Stress +{stress_add}.")

                        if mode_name == "Hooptie":
                            if random.random() < mode_data['breakdown_chance']:
                                print(Colors.RED + "The car broke down. You have to walk the rest of the way. +10 Stress." + Colors.RESET)
                                player.stress += 10

                        player.current_location = target
            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"An error occurred during travel: {e}")

            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice == "3":
            # Landmarks
            # Note: world_data structure for landmark is a string "landmark", not a list.
            lm = curr_loc_data.get('landmark')
            if not lm:
                print("No major landmark here.")
                input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)
            else:
                print_banner(lm, color=Colors.TEAL)
                desc = LANDMARK_FLAVOR.get(lm, "It's a place.")
                print(desc)
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

                elif lm in landmark_menus:
                    menu = landmark_menus[lm]
                    print(Colors.PINK + "--- MENU ---" + Colors.RESET)
                    items = list(menu.items())
                    for i, (k, v) in enumerate(items):
                        price = v[0]
                         # Gentrification Meter affects Coffee
                        if "Coffee" in k:
                            price = round(price * economy.GENTRIFICATION_METER, 2)
                        # Cheese Index affects any food with "Cheese", "Curd", "Pizza", "Burger"
                        elif any(x in k for x in ["Cheese", "Curd", "Pizza", "Burger"]):
                            price = round(price * economy.CHEESE_INDEX, 2)

                        print(f" {Colors.CYAN}{i+1}.{Colors.RESET} {k} ({Colors.YELLOW}${price:.2f}{Colors.RESET})")
                    
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
                            player.heal(vals[1])
                            player.relax(vals[2])
                            # Add item object if relevant
                            if "Coffee" in name or "Form" in name or "Override" in name:
                                # Create Item object
                                new_item = Item(name, vals[3], price, vals[1], vals[2])
                                player.add_item(new_item)
                            print(Colors.GREEN + f"You consumed {name}. {vals[3]}" + Colors.RESET)
                        else: print(Colors.RED + "Card Declined." + Colors.RESET)
                    except ValueError:
                         print("Invalid order.")
                    except IndexError:
                         print("Item not found.")

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
                client = clients_here[0] # Assuming one per loc for now
                print(f"Visiting {client.name}...")

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
                        print_banner("!!! THEY NEED HELP !!!", color=Colors.RED)
                        print(Colors.CYAN + "1. Intervene" + Colors.WHITE + " (Start Crisis Mode)")
                        print(Colors.CYAN + "2. Walk away" + Colors.WHITE + " (Stress +10)")
                        if input(Colors.PINK + "> " + Colors.RESET) == "1":
                            handle_crisis(player, client)
                        else:
                            player.stress += 10
                            print("You walk away.")
                    else:
                        print(Colors.GREEN + f"\nSTATUS: {text}" + Colors.RESET)
                        print(Colors.CYAN + "1. Hang out" + Colors.WHITE + " (-Stress, +Trust)")
                        if input(Colors.PINK + "> " + Colors.RESET) == "1":
                            player.relax(10)
                            player.update_client_relationship(client.name, trust_change=1, set_cooldown=3)
                            print(Colors.GREEN + "You vibe. It helps." + Colors.RESET)
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
                note = f"CD: {cd}" if cd > 0 else "READY"

                status_color = Colors.RED if status == "CRISIS" else Colors.GREEN
                print(f"{c.name:<15} | {loc:<15} | {status_color}{status:<10}{Colors.RESET} | {note}")
            print_separator(width=60, color=Colors.PINK)
            print(f"Billable Hours Pending: {Colors.YELLOW}{player.billable_hours}{Colors.RESET}")
            input(Colors.BRIGHT_BLACK + "\n[Press Enter]" + Colors.RESET)

        elif choice == "6":
            print_banner("INVENTORY", color=Colors.PINK)
            for item in player.inventory:
                print(f" {Colors.MAGENTA}*{Colors.RESET} {item.name if hasattr(item, 'name') else item}")
            input(Colors.BRIGHT_BLACK + "\n[Press Enter]" + Colors.RESET)

        elif choice == "7" and curr_loc_name == "The Center":
            if player.billable_hours > 0:
                print(f"Submitting {player.billable_hours} hours...")
                payout = economy.calculate_payout(player.billable_hours)
                player.modify_money(payout)
                player.billable_hours = 0
                print(f"You received {Colors.YELLOW}${payout:.2f}{Colors.RESET}.")
            else:
                print("You have no hours to bill. Get back to work.")
            input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

        elif choice == "8" and player.has_item("Ancient Coffee") and player.has_item("Forbidden Form 1040-X") and curr_loc_name == "Downtown":
             print(Colors.MAGENTA + ASCII_ART['KENNEDY'] + Colors.RESET)
             pantheon.summon_kennedy(player)
             input(Colors.BRIGHT_BLACK + "[Press Enter]" + Colors.RESET)

if __name__ == "__main__":
    main_game()
