"""
tumbleweave.py - The Tumbleweave Boss Battle System

The Tumbleweave is a legendary Milwaukee phenomenon - 
a weave that has detached from its owner and now blows 
through the streets with sentient malevolence.

Boss Battle Mechanics:
- Three phases: Drifting, Entangling, Transforming
- Weak to scissors but immune to logic
- Can inflict "Bad Hair Day" debuff
- Drops the Tumbleweave Trophy when defeated
"""

import random
import time
from typing import Optional

# Boss Phases
PHASE_DRIFTING = "drifting"
PHASE_ENTANGLING = "entangling"
PHASE_TRANSFORMING = "transforming"

# Attack patterns
class TumbleweaveAttack:
    """Represents an attack the Tumbleweave can use."""
    
    def __init__(self, name: str, damage: int, stress: int, description: str, phase: str):
        self.name = name
        self.damage = damage
        self.stress = stress
        self.description = description
        self.phase = phase

ATTACKS = [
    TumbleweaveAttack(
        "Hair Whip",
        damage=10,
        stress=15,
        description="The weave lashes out with synthetic fury!",
        phase=PHASE_DRIFTING
    ),
    TumbleweaveAttack(
        "Static Cling",
        damage=5,
        stress=25,
        description="It generates static electricity that makes your hair stand up!",
        phase=PHASE_DRIFTING
    ),
    TumbleweaveAttack(
        "Entangle",
        damage=15,
        stress=20,
        description="The weave wraps around your legs! You can't move!",
        phase=PHASE_ENTANGLING
    ),
    TumbleweaveAttack(
        "Bad Hair Day Curse",
        damage=0,
        stress=40,
        description="It inflicts a vision of your worst hair day! The horror!",
        phase=PHASE_ENTANGLING
    ),
    TumbleweaveAttack(
        "Synthetic Swarm",
        damage=25,
        stress=30,
        description="The weave splits into multiple strands that attack from all angles!",
        phase=PHASE_TRANSFORMING
    ),
    TumbleweaveAttack(
        "Identity Crisis",
        damage=20,
        stress=35,
        description="It questions your fashion choices with existential dread!",
        phase=PHASE_TRANSFORMING
    )
]

# Player moves specific to Tumbleweave battle
MOVE_SCISSORS = "brandish_scissors"
MOVE_LOGIC = "use_logic"
MOVE_WIND = "summon_wind"
MOVE_OPE_DODGE = "ope_dodge"
MOVE_COMPLIMENT = "compliment_weave"
MOVE_CAPTURE = "capture_in_bag"


class TumbleweaveBoss:
    """
    The legendary sentient hairpiece.
    """
    
    def __init__(self):
        self.name = "The Tumbleweave"
        self.max_hp = 150
        self.hp = 150
        self.phase = PHASE_DRIFTING
        self.phase_thresholds = {
            PHASE_DRIFTING: 100,  # Transitions at 100 HP
            PHASE_ENTANGLING: 50  # Transitions at 50 HP
        }
        self.turn_count = 0
        self.entangled = False  # Player is immobilized
        self.complimented = False  # Was complimented (weakens it)
        
    def is_alive(self) -> bool:
        return self.hp > 0
    
    def get_phase(self) -> str:
        """Returns current phase based on HP."""
        if self.hp > self.phase_thresholds[PHASE_DRIFTING]:
            return PHASE_DRIFTING
        elif self.hp > self.phase_thresholds[PHASE_ENTANGLING]:
            return PHASE_ENTANGLING
        else:
            return PHASE_TRANSFORMING
    
    def check_phase_transition(self) -> Optional[str]:
        """Check and handle phase transitions. Returns narrative text if phase changed."""
        new_phase = self.get_phase()
        
        if new_phase != self.phase:
            self.phase = new_phase
            
            if new_phase == PHASE_ENTANGLING:
                return """
*** PHASE TRANSITION: ENTANGLING ***
The Tumbleweave stops drifting and rises into the air!
It seems... angrier. More sentient.
The wind picks up. Plastic bags swirl around it like minions.
"""
            elif new_phase == PHASE_TRANSFORMING:
                return """
*** PHASE TRANSITION: TRANSFORMING ***
The Tumbleweave begins to glow with an unholy light!
It has achieved its final form - a perfect sphere of hair and fury!
You can hear whispered conversations from previous wearers...
"""
        
        return None
    
    def attack(self, player) -> str:
        """Execute an attack on the player. Returns narrative text."""
        # Get attacks available in current phase
        available_attacks = [a for a in ATTACKS if a.phase == self.phase]
        
        # If entangled, prefer entangling attacks
        if self.entangled:
            entangle_attacks = [a for a in available_attacks if "Entangle" in a.name]
            if entangle_attacks:
                attack = random.choice(entangle_attacks)
            else:
                attack = random.choice(available_attacks)
        else:
            attack = random.choice(available_attacks)
        
        # Apply damage
        if hasattr(player, 'stress'):
            player.stress += attack.stress
        if hasattr(player, 'hp'):
            player.hp -= attack.damage
        
        # Special effects
        if attack.name == "Entangle":
            self.entangled = True
        
        return f"\n>>> {attack.name} <<<\n{attack.description}\nStress +{attack.stress}, HP -{attack.damage}"
    
    def take_damage(self, amount: int, move_type: str) -> tuple:
        """
        Process damage to the Tumbleweave.
        Returns (actual_damage, narrative_text, was_critical)
        """
        was_critical = False
        
        # Weaknesses and resistances
        if move_type == MOVE_SCISSORS:
            amount = int(amount * 2.5)  # MASSIVE damage from scissors
            was_critical = True
            text = "The scissors SNIP through the weave! It SCREAMS! CRITICAL DAMAGE!"
        elif move_type == MOVE_LOGIC:
            amount = 0  # Immune to logic
            text = "You try to reason with the weave. It is hair. It does not understand logic."
        elif move_type == MOVE_WIND:
            amount = int(amount * 0.5)  # Resistant to wind
            text = "The wind makes it stronger! It feeds on air currents!"
        elif move_type == MOVE_COMPLIMENT:
            amount = int(amount * 1.5)
            self.complimented = True
            text = "The weave seems... flattered? Its guard drops!"
        elif move_type == MOVE_CAPTURE:
            amount = 20  # Good damage from bag capture
            text = "You try to bag it! It struggles but takes damage!"
        else:
            text = f"You attack for {amount} damage!"
        
        self.hp -= amount
        
        # Clear entangled if player did damage
        if amount > 0:
            self.entangled = False
        
        return amount, text, was_critical


def start_tumbleweave_battle(player) -> dict:
    """
    Main battle function. Returns battle results.
    """
    boss = TumbleweaveBoss()
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           ⚠️  BOSS ENCOUNTER: THE TUMBLEWEAVE  ⚠️                ║
║                                                                  ║
║     A weave detaches from an unseen head and rolls toward        ║
║     you with unnatural purpose. It has seen things.              ║
║     It has BEEN places. It wants YOU.                            ║
║                                                                  ║
║     HP: 150 | Phases: 3 | Weakness: SCISSORS                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    time.sleep(2)
    
    # Check for special items
    has_scissors = any("scissors" in (item.name if hasattr(item, 'name') else str(item)).lower() 
                      for item in player.inventory)
    has_bag = any("bag" in (item.name if hasattr(item, 'name') else str(item)).lower() 
                 for item in player.inventory)
    
    while boss.is_alive() and player.is_alive():
        print(f"\n{'='*60}")
        print(f"TUMBLEWEAVE HP: {boss.hp}/{boss.max_hp} | PHASE: {boss.phase.upper()}")
        print(f"YOUR STATUS: HP {player.hp} | STRESS {player.stress}")
        if boss.entangled:
            print("[ENTANGLED - Cannot use certain moves!]")
        print(f"{'='*60}")
        
        # Show available moves
        print("\nYour moves:")
        print("  1. Brandish Scissors" + (" (You don't have scissors!)" if not has_scissors else " ★ SUPER EFFECTIVE"))
        print("  2. Use Logic (Probably useless)")
        print("  3. Summon Wind")
        print("  4. The Ope [Dodge]")
        print("  5. Compliment the Weave")
        print("  6. Capture in Bag" + (" (You don't have a bag!)" if not has_bag else ""))
        
        # Get player choice
        choice = input("\n> ").strip()
        
        move_type = None
        base_damage = random.randint(15, 25)
        
        if choice == "1":
            if has_scissors:
                move_type = MOVE_SCISSORS
            else:
                print("You don't have scissors! You flap your hands uselessly!")
                move_type = "none"
        elif choice == "2":
            move_type = MOVE_LOGIC
        elif choice == "3":
            move_type = MOVE_WIND
        elif choice == "4":
            move_type = MOVE_OPE_DODGE
            print("Ope! Just gonna sneak past this sentient hair!")
            # Dodge mechanic
            if random.random() < 0.75:
                print("You successfully dodge! The weave tumbles past harmlessly!")
                # Player gets a free attack
                print("Counter-attack opportunity!")
                boss.hp -= 10
                print("You kick it while it's down! 10 damage!")
            else:
                print("You bumped into the weave! It's angry!")
            continue
        elif choice == "5":
            move_type = MOVE_COMPLIMENT
            print("'Nice... uh... volume?' you stammer.")
        elif choice == "6":
            if has_bag:
                move_type = MOVE_CAPTURE
            else:
                print("You don't have a bag! The weave laughs at your empty hands!")
                move_type = "none"
        else:
            print("Invalid choice! The weave attacks while you hesitate!")
        
        # Process player move
        if move_type and move_type != "none":
            damage, text, crit = boss.take_damage(base_damage, move_type)
            print(f"\n>>> {text}")
            if crit:
                print("*** CRITICAL HIT! ***")
            print(f"Dealt {damage} damage!")
        
        # Check phase transition
        phase_text = boss.check_phase_transition()
        if phase_text:
            print(phase_text)
            time.sleep(1)
        
        # Boss counter-attack if still alive
        if boss.is_alive():
            attack_text = boss.attack(player)
            print(attack_text)
        
        boss.turn_count += 1
        
        # Check for player defeat
        if not player.is_alive():
            print("""
╔══════════════════════════════════════════════════════════════════╗
║                    DEFEATED BY THE TUMBLEWEAVE                   ║
║                                                                  ║
║     You collapse under the weight of bad hair energy.            ║
║     The Tumbleweave rolls on, seeking its next victim...         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
            return {"victory": False, "reward": None}
        
        time.sleep(1)
    
    # Victory!
    if boss.hp <= 0:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                    ★ TUMBLEWEAVE DEFEATED! ★                     ║
║                                                                  ║
║     With a final SNIP of your scissors, the weave unravels!      ║
║     It dissolves into individual strands that blow away          ║
║     on the Milwaukee wind...                                     ║
║                                                                  ║
║     You are left holding: THE TUMBLEWEAVE TROPHY                 ║
║     A single strand of synthetic glory.                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
        
        # Create reward
        from engine import Item
        trophy = Item(
            name="Tumbleweave Trophy",
            description="A strand from the legendary sentient weave. It still twitches occasionally.",
            value=500,
            hp_restore=0,
            stress_relief=50
        )
        
        player.add_item(trophy)
        player.exp += 200
        
        # Mint crypto token
        try:
            from save_system import token_registry
            token = token_registry.mint_token("Tumbleweave Slayer", player.name)
            if token:
                print(f"\n🏆 CRYPTO TROPHY MINTED!")
                print(f"Token ID: {token['token_id']}")
                print(f"You are now a certified Tumbleweave Slayer!")
        except:
            pass
        
        return {"victory": True, "reward": trophy}
    
    return {"victory": False, "reward": None}


def check_tumbleweave_encounter(player) -> bool:
    """
    Random chance to trigger Tumbleweave encounter.
    Returns True if battle was triggered and completed.
    """
    # 2% chance per explore
    if random.random() < 0.02:
        result = start_tumbleweave_battle(player)
        return result["victory"]
    return False


# Tumbleweave Slayer token for crypto registry
TUMBLEWEAVE_TOKEN_CONFIG = {
    "Tumbleweave Slayer": {
        "description": "Proof of defeating the legendary sentient weave of Milwaukee.",
        "rarity": "Legendary",
        "max_supply": 414  # Only 414 slayers can exist
    }
}
