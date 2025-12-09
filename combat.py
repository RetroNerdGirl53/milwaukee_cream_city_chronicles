import random

# --- ENEMY CLASS ---
class Enemy:
    """
    Defines the Enemy class with specific types and attributes.
    """
    TYPE_STONEWALLER = 'Stonewaller' # High Defense, uses 'Please Hold'
    TYPE_AGGRESSOR = 'Aggressor'     # High Damage
    TYPE_DRAINER = 'Drainer'         # Steals XP/Time

    TYPES = [TYPE_STONEWALLER, TYPE_AGGRESSOR, TYPE_DRAINER]

    def __init__(self, name, enemy_type, hp):
        self.name = name
        if enemy_type not in self.TYPES:
            # Fallback or default
            enemy_type = self.TYPE_STONEWALLER
        self.type = enemy_type
        self.hp = hp
        self.max_hp = hp

    def is_alive(self):
        return self.hp > 0

    def attack_player(self, player):
        """
        Executes the enemy's attack on the player based on enemy type.
        """
        if self.type == self.TYPE_STONEWALLER:
            # Stonewaller uses delays and blocks
            roll = random.random()
            if roll < 0.5:
                # "Please Hold" - Stuns/Delays (Simulated by high stress)
                dmg = random.randint(5, 10)
                print(f"{self.name} uses 'Please Hold'. The hold music is distorted and loops endlessly. You are stunned by the inefficiency. (Stress +{dmg})")
                player.stress += dmg
            else:
                 # "Fax Required" - Heavy Stress Damage
                 dmg = random.randint(15, 20)
                 print(f"{self.name} demands a 'Fax Required'. You don't have a fax machine. Panic sets in. (Stress +{dmg})")
                 player.stress += dmg

        elif self.type == self.TYPE_AGGRESSOR:
            # Aggressor uses High Damage
            roll = random.random()
            if roll < 0.5:
                # "Intimidation Tactics" - Heavy Stress
                dmg = random.randint(15, 25)
                print(f"{self.name} uses 'Intimidation Tactics'. It's super effective! (Stress +{dmg})")
                player.stress += dmg
            else:
                # Physical/Kia Boy related damage (if HP damage was distinct from stress, but here we mostly track stress in combat loop examples, but let's assume HP damage is possible too or just generic 'damage')
                # The prompt implies mostly Stress mechanics in text, but let's do generic damage.
                # Actually devdoc says "Kia Boys: You lose 10 years of your life (Stress +10)"
                dmg = random.randint(10, 20)
                print(f"{self.name} swerves wildly on the sidewalk. You dodge for your life. (Stress +{dmg})")
                player.stress += dmg

        elif self.type == self.TYPE_DRAINER:
            # Drainer uses XP/Time theft
            roll = random.random()
            if roll < 0.6:
                # "Meeting That Could Have Been An Email"
                print(f"{self.name} uses 'Meeting That Could Have Been An Email'.")
                if hasattr(player, 'exp') and player.exp > 0:
                    drain = 10
                    player.exp = max(0, player.exp - drain)
                    print(f"You feel your life experience draining away... (-{drain} XP)")
                player.stress += 5
            else:
                # "Passive Aggressive Note" - Low damage, lowers Morale (Stress)
                dmg = random.randint(5, 8)
                print(f"{self.name} leaves a 'Passive Aggressive Note' on your desk regarding the breakroom fridge. (Stress +{dmg})")
                player.stress += dmg

# --- PLAYER MOVES ---
MOVE_MALICIOUS_COMPLIANCE = 'Malicious Compliance'
MOVE_WEAPONIZED_APATHY = 'Weaponized Apathy'
MOVE_JARGON_OVERLOAD = 'Jargon Overload'
MOVE_THE_OPE = 'The Ope'
MOVE_CONTEXTUAL = 'Contextual'

PLAYER_MOVES = [
    MOVE_MALICIOUS_COMPLIANCE,
    MOVE_WEAPONIZED_APATHY,
    MOVE_JARGON_OVERLOAD,
    MOVE_THE_OPE,
    MOVE_CONTEXTUAL
]

# Satirical Contextual Moves
# Format: (Name, Flavor Text, Damage)
SATIRICAL_MOVES = [
    ("Dateline Quote", "You mention you saw them on Dateline. It gets awkward.", 20),
    ("Roundabout Explanation", "You explain how to navigate a roundabout correctly. They are confused.", 15),
    ("Fish Fry Distraction", "You toss a Fish Fry at them. They are compelled to eat it.", 25),
    ("Tavern League Law", "You cite obscure tavern laws. It's super effective.", 30),
    ("Pot Hole Trap", "You lure them into a crater-sized pothole.", 35),
    ("Weather Complaint", "You complain about the humidity. They agree, losing their will to fight.", 10),
    ("Brandy Old Fashioned", "You mix a drink. It muddles their senses.", 20)
]

def get_random_contextual_move(enemy):
    """
    Returns a random contextual move, potentially specific to the enemy.
    """
    # Specific moves based on enemy name keywords (expanding on scenarios)
    specific_moves = []
    if "Roomba" in enemy.name:
        specific_moves.append(("Firmware Update", "You force a firmware update. It reboots.", 40))
    if "Ticket" in enemy.name:
        specific_moves.append(("Contest in Court", "You threaten to go to court. It shudders.", 30))
    if "Yeast" in enemy.name or "Sourdough" in enemy.name:
        specific_moves.append(("Over-Proofing", "You turn up the heat. It rises too fast and collapses.", 35))
    if "Inspector" in enemy.name:
        specific_moves.append(("Permit flash", "You show a permit from 1982. It checks out.", 25))

    # Combine with generic satirical moves
    pool = SATIRICAL_MOVES + specific_moves
    move = random.choice(pool)
    return move

def resolve_turn(player, enemy, move_choice):
    """
    Calculates damage based on match-ups and updates player/enemy state.
    """
    print(f"\n--- {player.name} vs {enemy.name} ({enemy.type}) ---")

    player_damage = 0
    flavor = ""
    dodge = False

    # Resolve Player Move
    if move_choice == MOVE_MALICIOUS_COMPLIANCE:
        base_dmg = random.randint(15, 25)
        flavor = "You follow their instructions EXACTLY." # Matches prompt/devdoc spirit
        # Original flavor: "You cite a regulation from 1974. It's super effective."
        # Merged flavor:
        flavor += " You cite a regulation from 1974. It's super effective."

        if enemy.type == Enemy.TYPE_STONEWALLER:
            player_damage = int(base_dmg * 2.0) # Crit vs Bureaucracy
            flavor += " CRITICAL HIT! The Stonewaller drowns in their own red tape!"
        else:
            player_damage = base_dmg

    elif move_choice == MOVE_WEAPONIZED_APATHY:
        base_dmg = random.randint(10, 20)
        flavor = "You stare blankly. You do not blink."
        # Original flavor: "You sigh aggressively. The enemy feels awkward."
        flavor += " You sigh aggressively."

        if enemy.type == Enemy.TYPE_AGGRESSOR:
            player_damage = int(base_dmg * 2.0) # Crit vs Aggressor/Emotional
            flavor += " CRITICAL HIT! The Aggressor is starved of attention!"
        else:
            player_damage = base_dmg

    elif move_choice == MOVE_JARGON_OVERLOAD:
        base_dmg = random.randint(10, 20)
        flavor = "You unleash a torrent of buzzwords: 'Synergy', 'Circle Back', 'Holistic'."
        # Original flavor: "You say 'Circle Back' and 'Synergy' until their ears bleed."

        if enemy.type == Enemy.TYPE_DRAINER:
            player_damage = int(base_dmg * 2.0) # Crit vs Drainer/Corporate
            flavor += " CRITICAL HIT! You out-drain the Drainer!"
        else:
            player_damage = base_dmg

    elif move_choice == MOVE_THE_OPE:
        flavor = "Ope! Just gonna sneak right past ya there."
        dodge = True

    elif move_choice == MOVE_CONTEXTUAL:
        move_name, move_flavor, move_dmg = get_random_contextual_move(enemy)
        flavor = f"[{move_name}] {move_flavor}"
        player_damage = move_dmg
        # Small chance for critical on contextual
        if random.random() > 0.8:
            player_damage = int(player_damage * 1.5)
            flavor += " (It's super effective!)"

    # Apply Player Damage
    if player_damage > 0:
        # Stonewaller Defense check (High Defense)
        # If the move wasn't a crit (Malicious Compliance), reduce damage
        if enemy.type == Enemy.TYPE_STONEWALLER and move_choice != MOVE_MALICIOUS_COMPLIANCE:
             player_damage = int(player_damage * 0.5)
             flavor += " (Reduced by Red Tape Defense)"

        print(f"> {flavor}")
        enemy.hp -= player_damage
        print(f"> You dealt {player_damage} damage.")
    elif move_choice == MOVE_THE_OPE:
        print(f"> {flavor}")

    # Enemy Turn
    if enemy.is_alive():
        if dodge:
            # 75% chance to dodge
            if random.random() < 0.75:
                print(f"> {enemy.name} attacks, but you Oped out of the way!")
            else:
                print(f"> You tried to Ope, but bumped into them.")
                enemy.attack_player(player)
        else:
            enemy.attack_player(player)

    print(f"Status: Enemy HP {enemy.hp} | Player Stress {player.stress}")
