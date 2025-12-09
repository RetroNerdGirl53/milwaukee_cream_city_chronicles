import random
import time
import pantheon

# --- THE SACRED TEXTS ---
def play_intro():
    print("\n" + "*"*70)
    print("IN THE BEGINNING, THERE WAS THE MILVERINE.")
    print("He walked the 414 when others drove. He wore the shorts in January.")
    print("AND IN THE SHADOWS, THERE WAS KENNEDY.")
    print("The Sorceress of the System. The High Priestess of 'Per My Last Email'.")
    print("\nWELCOME TO MILWAUKEE.")
    print("Where the beer is cold, the cheese is loud, and the bureaucracy is hungry.")
    print("*"*70 + "\n")
    time.sleep(2)

# --- THE MENUS (SATIRE EDITION) ---
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

# --- CLIENT SYSTEM ---
class Client:
    def __init__(self, name, location, chill_scenarios, crisis_scenarios, enemy_data):
        self.name = name
        self.location = location
        self.chill_scenarios = chill_scenarios
        self.crisis_scenarios = crisis_scenarios
        self.enemy_data = enemy_data

        # State
        self.status = "Chill" # or "Crisis"
        self.cooldown = 0
        self.current_scenario_text = self._get_random_text(self.chill_scenarios)

    def _get_random_text(self, scenarios):
        # scenarios is a list of tuples (State, Text) or just strings?
        # Looking at original code: ("Chill", "Text")
        # So we just want the text part
        return random.choice([s[1] for s in scenarios])

    def update_turn(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            if self.cooldown == 0:
                # Cooldown expired.
                pass # Ready for new crisis?

        # If chill and no cooldown, small chance to go crisis
        if self.status == "Chill" and self.cooldown == 0:
            if random.random() < 0.2: # 20% chance per turn
                self.trigger_crisis()

    def trigger_crisis(self):
        self.status = "Crisis"
        self.current_scenario_text = self._get_random_text(self.crisis_scenarios)

    def resolve_crisis(self):
        self.status = "Chill"
        self.cooldown = random.randint(3, 6) # Safe for a few turns
        self.current_scenario_text = self._get_random_text(self.chill_scenarios)

    def get_info_line(self):
        status_color = "CRITICAL" if self.status == "Crisis" else "STABLE"
        cd_text = f"(CD: {self.cooldown})" if self.cooldown > 0 else "(READY)"
        return f"[{status_color}] {self.name} ({self.location}) {cd_text}"

class Caseload:
    def __init__(self):
        self.clients = {}
        self._init_clients()

    def _init_clients(self):
        # Define clients here (moved from get_client_scenario)

        # Chloe
        self.clients["Chloe"] = Client(
            "Chloe", "Polonia",
            [("Chill", "Chloe is eating pierogis while coding on a laptop from 1999."),
             ("Chill", "Chloe is in the basement trying to rewire the Basilica's bells.")],
            [("Crisis", "Chloe accidentally hacked the Mayor's fridge and the Feds are outside."),
             ("Crisis", "Chloe's homemade server farm melted the fuse box.")],
            {"name": "Sentient Roomba", "hp": 50, "weakness": "Logic"}
        )

        # Bobbie
        self.clients["Bobbie"] = Client(
            "Bobbie", "West Allis",
            [("Chill", "Bobbie is polishing his Dale Earnhardt commemorative plates."),
             ("Chill", "Bobbie is asleep in a recliner from 1985.")],
            [("Crisis", "Bobbie is fighting a 'Demon' in his closet (it's unpaid parking tickets)."),
             ("Crisis", "Bobbie bought 400lbs of birdseed on QVC and is trapped.")],
            {"name": "The Ticket Demon", "hp": 60, "weakness": "Paperwork"}
        )

        # Liam
        self.clients["Liam"] = Client(
            "Liam", "Bay View",
            [("Chill", "Liam is waxing his mustache and listening to a band that doesn't exist yet."),
             ("Chill", "Liam offers you a deconstructed coffee. It's just beans and hot water separately.")],
            [("Crisis", "Liam's sourdough starter has grown too large and is consuming the kitchen."),
             ("Crisis", "Liam is having a panic attack because he saw someone wearing cargo shorts.")],
            {"name": "The Sourdough Monster", "hp": 45, "weakness": "Apathy"}
        )

        # Mrs. Higgins
        self.clients["Mrs. Higgins"] = Client(
            "Mrs. Higgins", "Sherman Park",
            [("Chill", "Mrs. Higgins feeds you sweet potato pie until you can't move."),
             ("Chill", "Mrs. Higgins is watching her stories (Soap Operas) at max volume.")],
            [("Crisis", "The City hasn't fixed the pothole in front of her house. She is ready for war."),
             ("Crisis", "Her grandson installed 'The TikTok' on her phone and she is confused.")],
            {"name": "The City Inspector", "hp": 80, "weakness": "Paperwork"}
        )

        # Tyler
        self.clients["Tyler"] = Client(
            "Tyler", "East Side",
            [("Chill", "Tyler is playing hacky-sack. It is 2025. You are confused."),
             ("Chill", "Tyler is asleep in the library. He has drooled on a textbook.")],
            [("Crisis", "Tyler has to write a 40-page thesis by tomorrow. He hasn't started."),
             ("Crisis", "Tyler forgot to pay his tuition and is about to be expelled.")],
            {"name": "The Looming Deadline", "hp": 40, "weakness": "Logic"}
        )

    def get_client(self, name):
        return self.clients.get(name)

    def update_all(self):
        for client in self.clients.values():
            client.update_turn()

    def print_manifest(self):
        print("\n" + "="*50)
        print("COUNTY CASELOAD MANIFEST (CONFIDENTIAL)")
        print("SYSTEM STATUS: OVERBURDENED")
        print("="*50)
        print(f"{'CLIENT':<15} | {'LOC':<15} | {'STATUS':<10} | {'NOTES'}")
        print("-" * 70)
        for name, c in self.clients.items():
            status = c.status.upper()
            note = "NEEDS VISIT" if status == "CRISIS" else "Monitoring..."
            if c.cooldown > 0: note = f"Safe for {c.cooldown} turns"
            print(f"{name:<15} | {c.location:<15} | {status:<10} | {note}")
        print("="*50)
        print("Use 'Visit Client' to intervene.\n")


# --- PLAYER CLASS ---
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.stress = 0
        self.max_stress = 100
        self.money = 60.00
        self.exp = 0
        self.current_location = "Downtown"
        self.inventory = [] 
        self.blessed_by_milverine = False 
        self.caseload = Caseload() # Player has a caseload now

    def is_alive(self):
        return self.hp > 0 and self.stress < self.max_stress

    def check_milverine_save(self):
        # Delegate to pantheon module
        return pantheon.check_milverine_intervention(self)

    def modify_money(self, amount):
        self.money += amount
        if self.money < 0:
            print("   -> BANK ALERT: Overdraft ($35). Being poor is expensive.")
            self.money -= 35

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def relax(self, amount):
        self.stress = max(0, self.stress - amount)

# --- COMBAT / CRISIS SYSTEM ---
def resolve_crisis(player, client):
    enemy = client.enemy_data
    print(f"\n--- CONFRONTING: {enemy['name']} ---")
    enemy_hp = enemy['hp']
    
    if "Administrative Override" in player.inventory:
        print("\n[?] Invoke Kennedy's ADMINISTRATIVE OVERRIDE? (y/n)")
        if input("> ") == "y":
            print("\n*** KENNEDY'S WRATH ***")
            print("A giant spectral rubber stamp descends from the sky.")
            print("IT READS: 'NOT MY PROBLEM'.")
            print(f"The {enemy['name']} is instantly filed away.")
            player.inventory.remove("Administrative Override")
            player.exp += 50
            client.resolve_crisis() # Success
            return

    while enemy_hp > 0 and player.is_alive():
        print(f"Enemy Intensity: {enemy_hp} | Stress: {player.stress}")
        print("1. Malicious Compliance (Use rules against them)")
        print("2. Weaponized Apathy (Stare blankly)")
        print("3. Bureaucratic Jargon (Confuse them)")
        
        try:
            choice = input("> ")
            damage = 0
            flavor = ""
            
            if choice == "1":
                damage = random.randint(15, 25)
                flavor = "You cite a regulation from 1974. It's super effective."
                if enemy['weakness'] == "Paperwork": damage *= 2
            elif choice == "2":
                damage = random.randint(5, 15)
                flavor = "You sigh aggressively. The enemy feels awkward."
                if enemy['weakness'] == "Apathy": damage *= 2
            elif choice == "3":
                damage = random.randint(10, 20)
                flavor = "You say 'Circle Back' and 'Synergy' until their ears bleed."
                if enemy['weakness'] == "Logic": damage *= 2
            
            print(f"> {flavor}")
            enemy_hp -= damage
            
            if enemy_hp > 0:
                print(f"> {enemy['name']} strikes back! Stress +10")
                player.stress += 10
                if player.check_milverine_save():
                    client.resolve_crisis() # Saved by Milverine counts as resolved? Maybe not.
                    return
        except: pass

    if player.is_alive():
        print("Crisis Resolved.")
        billable_hours = random.randint(3, 8)
        print(f"Billed {billable_hours} hours to The Center...")
        payment = economy.calculate_payout(billable_hours)
        player.exp += 50
        player.modify_money(loot)
        print(f"You billed the state for ${loot}.")
        client.resolve_crisis()

# --- THE EXPANSIVE MAP (UPDATED) ---
milwaukee_map = {
    "Downtown": {
        "desc": "Skyscrapers, sadness, and the Library.",
        "neighbors": ["East Side", "Riverwest", "Walker's Point", "Third Ward", "Near West Side"],
        "landmarks": ["The Safe House", "Central Library", "El Trucko"],
        "clients": []
    },
    "Third Ward": {
        "desc": "Expensive condos and boutiques you are too poor to enter.",
        "neighbors": ["Downtown", "Walker's Point"],
        "landmarks": ["Milwaukee Public Market", "Wicked Hop"],
        "clients": []
    },
    "Riverwest": {
        "desc": "Alleys, art, anarchy, and very tight pants.",
        "neighbors": ["East Side", "Downtown", "Bronzeville"],
        "landmarks": ["Falcon Bowl", "Art Bar"],
        "clients": [] # Chloe moved!
    },
    "Polonia": {
        "desc": "The historic South Side. The Basilica looms over everything. Smells like incense and old bricks.",
        "neighbors": ["Walker's Point", "Bay View"],
        "landmarks": ["Basilica of St. Josaphat", "Kosciuszko Park"],
        "clients": ["Chloe"] # Chloe is here now
    },
    "Walker's Point": {
        "desc": "Industrial chic. Smells like chocolate or sewage.",
        "neighbors": ["Downtown", "Bay View", "Third Ward", "Polonia"],
        "landmarks": ["Sobelman's", "Conejito's Place"],
        "clients": []
    },
    "Bay View": {
        "desc": "Hipster parents pushing $800 strollers.",
        "neighbors": ["Walker's Point", "Polonia"],
        "landmarks": ["The Vanguard", "Small Pie"],
        "clients": ["Liam"]
    },
    "East Side": {
        "desc": "Impossible parking. UWM students. The scent of Lake Michigan.",
        "neighbors": ["Downtown", "Riverwest"],
        "landmarks": ["Wolski's", "Ma Fischer's"],
        "clients": ["Tyler"]
    },
    "Near West Side": {
        "desc": "Marquette University and the highway.",
        "neighbors": ["Downtown", "Speed Queen Area", "Bronzeville"],
        "landmarks": ["Real Chili", "The Rave"],
        "clients": []
    },
    "Speed Queen Area": {
        "desc": "The air here smells like smoked meat. It is holy ground.",
        "neighbors": ["Near West Side", "Sherman Park", "Bronzeville"],
        "landmarks": ["Speed Queen BBQ"],
        "clients": []
    },
    "Sherman Park": {
        "desc": "Historic homes and beautiful boulevards.",
        "neighbors": ["Speed Queen Area", "Wauwatosa"],
        "landmarks": ["Sherman Phoenix"],
        "clients": ["Mrs. Higgins"]
    },
    "West Allis": {
         "desc": "Stallis. The land of honest people and questionable lawn ornaments.",
         "neighbors": ["Wauwatosa", "Hales Corners"],
         "landmarks": ["West Allis Cheese Shoppe"],
         "clients": ["Bobbie"]
    },
    "Wauwatosa": {
        "desc": "The suburbs. It's quiet. Too quiet.",
        "neighbors": ["Sherman Park", "West Allis"],
        "landmarks": ["Gilles Frozen Custard"],
        "clients": []
    },
    "Hales Corners": {
        "desc": "Southwest side. Neon lights glow in the distance.",
        "neighbors": ["West Allis"],
        "landmarks": ["Leon's Frozen Custard"],
        "clients": []
    },
    "Bronzeville": {
        "desc": "Culture, business, and history.",
        "neighbors": ["Riverwest", "Near West Side", "Speed Queen Area"],
        "landmarks": ["Gee's Clippers"],
        "clients": []
    },
    "The Center": {
        "desc": "The Coggs Center. The heart of darkness.",
        "neighbors": ["Downtown"],
        "landmarks": [],
        "clients": [],
        "danger_bonus": 20
    }
}

# --- MAIN LOOP ---
def main_game():
    play_intro()
    p_name = input("Enter Case Worker Name: ")
    player = Player(p_name)
    
    while True:
        if not player.is_alive():
            if not player.check_milverine_save(): 
                print("GAME OVER. You moved to Madison.")
                break

        # Update clients every turn
        player.caseload.update_all()

        curr = milwaukee_map[player.current_location]
        print(f"\nLOC: {player.current_location.upper()} | HP: {player.hp} | STRESS: {player.stress}")
        if "Administrative Override" in player.inventory: print("STATUS: PROTECTED BY KENNEDY")
        if player.blessed_by_milverine: print("STATUS: BLESSED BY THE MILVERINE")
        
        print(f"DESC: {curr['desc']}")
        print("1. Explore (Risk Encounter)")
        print("2. Travel")
        print("3. Visit Landmark")
        print("4. Visit Client")
        print("5. View Caseload (Client Info)")
        if "Ancient Coffee" in player.inventory and "Forbidden Form 1040-X" in player.inventory:
            print("6. !!! SUMMON KENNEDY !!!")

        choice = input("> ")
        
        if choice == "1":
            roll = random.randint(1, 100)
            if roll >= 95: 
                print("\n*** THE MILVERINE WALKS PAST. YOU ARE BLESSED. ***")
                player.blessed_by_milverine = True
                player.stress = 0
            elif roll >= 85:
                pantheon.invoke_freeway(player)
            elif roll < 10:
                print("\n*** ENCOUNTER: TUMBLEWEAVE ***")
                print("A weave blows past you like a western movie. It's majestic.")
            elif roll < 30:
                print("\n*** ENCOUNTER: KIA BOYS ***")
                print("A car drives on the sidewalk. You dodge. Stress +10.")
                player.stress += 10
            elif roll < 50:
                print("\n*** ENCOUNTER: CONSTRUCTION ***")
                print("The road is closed. It has been closed since 2004.")
                player.stress += 5
            else:
                print(f"You walk through {player.current_location}. You see a 'Re-Elect Tom Barrett' sticker fading on a light pole.")

        elif choice == "2":
            dests = curr['neighbors']
            for i, d in enumerate(dests): print(f"{i+1}. {d}")
            try: 
                c = int(input("> ")) - 1
                if 0 <= c < len(dests):
                    print("Waiting for the bus...")
                    economy.update_market_vibes()

                    if random.random() > 0.8:
                        print("The bus is late. Obviously.")
                        player.stress += 5

                    # Pothole Index affects travel comfort
                    if economy.POTHOLE_INDEX > 1.5:
                        print("Due to massive potholes, the bus bounces violently. +2 Stress")
                        player.stress += 2

                    player.current_location = dests[c]
                    player.modify_money(-2.25)
            except: pass

        elif choice == "3":
            lms = curr.get('landmarks', [])
            for i, l in enumerate(lms): print(f"{i+1}. {l}")
            try:
                target = lms[int(input("> "))-1]

                if target == "El Trucko":
                     el_trucko.update_hype()
                     menu_items = el_trucko.display_menu() # returns list of (item, price)

                     sel = int(input("Order > "))-1
                     name, price = menu_items[sel]

                     if player.money >= price:
                         player.modify_money(-price)
                         player.heal(10)
                         player.relax(5)
                         print(f"You ate {name}. It was trendy.")
                     else:
                         print("Too expensive for your budget.")

                elif target in landmark_menus:
                    menu = landmark_menus[target]
                    print(f"--- {target.upper()} ---")
                    items = list(menu.items())
                    for i, (k, v) in enumerate(items):
                        price = v[0]
                        # Gentrification Meter affects Coffee
                        if "Coffee" in k:
                            price = round(price * economy.GENTRIFICATION_METER, 2)
                        # Cheese Index affects any food with "Cheese", "Curd", "Pizza", "Burger"
                        elif any(x in k for x in ["Cheese", "Curd", "Pizza", "Burger"]):
                            price = round(price * economy.CHEESE_INDEX, 2)

                        print(f"{i+1}. {k} (${price})")
                    
                    sel = int(input("Order > "))-1
                    name, vals = items[sel]
                    
                    price = vals[0]
                    if "Coffee" in name:
                        price = round(price * economy.GENTRIFICATION_METER, 2)
                    elif any(x in name for x in ["Cheese", "Curd", "Pizza", "Burger"]):
                        price = round(price * economy.CHEESE_INDEX, 2)

                    if player.money >= price:
                        player.modify_money(-price)
                        player.heal(vals[1])
                        player.relax(vals[2])
                        if "Coffee" in name or "Form" in name or "Override" in name:
                            player.inventory.append(name)
                        print(f"You consumed {name}. {vals[3]}")
                    else: print("Card Declined. Awkward.")
            except: pass

        elif choice == "4":
            clients_in_loc = curr['clients']
            if not clients_in_loc: print("No clients live here.")
            else:
                client_name = clients_in_loc[0]
                client = player.caseload.get_client(client_name)
                
                print(f"Visiting {client.name}...")
                print(f"\nSTATUS: {client.current_scenario_text}")

                if client.status == "Crisis":
                    print("!!! THEY NEED HELP !!!")
                    print("1. Intervene (Start Crisis Mode)")
                    print("2. Walk away (Stress +10)")
                    if input("> ") == "1":
                        resolve_crisis(player, client)
                    else:
                        player.stress += 10
                        print("You walk away, feeling the guilt of a thousand case workers.")
                else:
                    print("1. Hang out (-Stress)")
                    if input("> ") == "1":
                        player.relax(10)
                        print("You vibe. It helps.")

        elif choice == "5":
elif choice == "5":
            player.caseload.print_manifest()

        elif choice == "6":
            # Use the cleaner logic from the pantheon module
            pantheon.summon_kennedy(player)
if __name__ == "__main__":
    main_game()
