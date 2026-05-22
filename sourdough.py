"""
sourdough.py - The Sentient Sourdough Companion System

A cursed companion that evolves, mutates, and reproduces.
Based on the legendary sourdough starter from the game's lore.
"""

import random
import time
from typing import Optional, List, Dict, Any

# Mutation Forms
FORM_PUDDLE = "The Puddle"
FORM_PARTNER = "The Partner"
FORM_COMPASS = "The Compass"
FORM_VOID = "The Void"
FORM_HOMUNCULUS = "The Homunculus"
FORM_CRITIC = "The Critic"
FORM_ORACLE = "The Oracle"

ALL_FORMS = [FORM_PUDDLE, FORM_PARTNER, FORM_COMPASS, FORM_VOID, FORM_HOMUNCULUS, FORM_CRITIC, FORM_ORACLE]

# Form descriptions for narrative
FORM_LORE = {
    FORM_PUDDLE: "It has become a sentient puddle of gluten. It glistens with malice.",
    FORM_PARTNER: "It has assumed a humanoid shape. It looks at you with rye-flour eyes.",
    FORM_COMPASS: "It pulses with directional energy. It points toward 'The Bread Dimension'.",
    FORM_VOID: "It has become a dark sourdough singularity. You can see through it to somewhere else.",
    FORM_HOMUNCULUS: "A tiny bread-person stares at you. It is hungry. It is always hungry.",
    FORM_CRITIC: "It has developed a face made of crust. It judges your purchases harshly.",
    FORM_ORACLE: "It bubbles with ancient wisdom. You understand the language of pigeons now."
}

# Form mechanics
FORM_EFFECTS = {
    FORM_PUDDLE: {
        "slide_chance": 0.05,  # 5% chance to slide to random location
        "description": "May slide to neighboring locations"
    },
    FORM_PARTNER: {
        "relationship_status": "It's Complicated",
        "stress_bonus": -5,  # Being in a relationship with bread is weirdly comforting
        "date_available": True,
        "description": "You are in a relationship with sourdough"
    },
    FORM_COMPASS: {
        "unlocks_fast_travel": True,
        "fast_travel_destination": "The Bread Dimension",
        "description": "Unlocks fast travel to The Bread Dimension"
    },
    FORM_VOID: {
        "spectral_sight": True,  # See hidden things
        "description": "Reveals hidden flavor text and secrets"
    },
    FORM_HOMUNCULUS: {
        "consumes_food_daily": True,
        "food_consumption": 1,  # Eats 1 food item per day
        "description": "Consumes 1 food item from inventory daily"
    },
    FORM_CRITIC: {
        "insults_purchases": True,
        "discount_chance": 0.10,  # 10% chance vendors give discount to stop the insults
        "description": "May get discounts by intimidating vendors"
    },
    FORM_ORACLE: {
        "understands_animals": True,
        "random_wisdom": True,  # Gives random hints
        "description": "Understands pigeons and squirrels; gives cryptic hints"
    }
}


class SentientSourdough:
    """
    A living sourdough starter that evolves and causes chaos.
    """
    
    def __init__(self, generation: int = 0, name: str = "The Starter"):
        self.name = name
        self.generation = generation  # 0 = Original, 1 = Child, 2 = Grandchild
        self.form = FORM_PUDDLE  # Starts as puddle
        self.stickiness = float('inf')  # Cannot be dropped (lore-wise)
        self.is_cursed = True
        self.age_turns = 0
        self.mutation_timer = random.randint(10, 15)  # Mutates every 10-15 turns
        self.reproduction_ready = False
        self.children_produced = 0
        self.merged_into_elder = False
        
        # Stats affected by form
        self.hunger = 0  # For Homunculus form
        
    def __repr__(self):
        return f"<SentientSourdough: {self.name} (Gen {self.generation}, {self.form})>"
    
    def advance_turn(self) -> Optional[str]:
        """
        Call this each game turn. Handles aging, mutation checks.
        Returns event text if something happens, None otherwise.
        """
        self.age_turns += 1
        self.mutation_timer -= 1
        events = []
        
        # Check for mutation
        if self.mutation_timer <= 0:
            event = self.mutate()
            if event:
                events.append(event)
            self.mutation_timer = random.randint(10, 15)  # Reset timer
        
        # Check reproduction (Gen 0 and 1 can reproduce)
        if self.generation < 2 and self.age_turns > 20 and not self.reproduction_ready:
            self.reproduction_ready = True
            events.append(f"{self.name} is bubbling vigorously... it's ready to reproduce!")
        
        # Form-specific daily effects
        if self.form == FORM_HOMUNCULUS:
            self.hunger += 1
            if self.hunger >= 3:
                events.append(f"{self.name} (The Homunculus) is VERY hungry and eyeing your supplies...")
        
        if self.form == FORM_PARTNER and self.age_turns % 10 == 0:
            events.append(f"{self.name} sends you a text: 'we need to talk about our flour-ture'")
        
        if self.form == FORM_ORACLE and random.random() < 0.2:
            wisdom = self._get_oracle_wisdom()
            events.append(f"{self.name} bubbles wisdom: '{wisdom}'")
        
        return "\n".join(events) if events else None
    
    def mutate(self) -> Optional[str]:
        """
        Triggers a mutation. Changes form randomly.
        Returns narrative text of the mutation.
        """
        old_form = self.form
        
        # Weighted random selection (some forms are rarer)
        weights = [
            (FORM_PUDDLE, 20),
            (FORM_PARTNER, 10),
            (FORM_COMPASS, 10),
            (FORM_VOID, 5),
            (FORM_HOMUNCULUS, 15),
            (FORM_CRITIC, 20),
            (FORM_ORACLE, 10)
        ]
        
        forms, w = zip(*weights)
        self.form = random.choices(forms, weights=w)[0]
        
        # Special narrative for Partner -> Breakup
        if old_form == FORM_PARTNER and self.form != FORM_PARTNER:
            return f"*** THE BREAKUP ***\n{self.name} leaves you a note written in flour:\n'It's not you, it's gluten. We're through.'\n\nIt mutates into {self.form}!\n{FORM_LORE[self.form]}"
        
        # Special narrative for becoming Partner
        if self.form == FORM_PARTNER and old_form != FORM_PARTNER:
            return f"*** A BREAD RELATIONSHIP BEGINS ***\n{self.name} shifts into {self.form}!\n{FORM_LORE[self.form]}\n\nYour relationship status is now: '{FORM_EFFECTS[FORM_PARTNER]['relationship_status']}'"
        
        # Standard mutation
        if self.form != old_form:
            return f"*** MUTATION! ***\n{self.name} bubbles violently and transforms!\nIt is now {self.form}.\n{FORM_LORE[self.form]}"
        
        return None
    
    def reproduce(self) -> Optional['SentientSourdough']:
        """
        Mitosis - creates a baby sourdough.
        Gen 0 -> 2 babies, Gen 1 -> 2 babies, Gen 2 -> sterile
        Returns new SentientSourdough or None if can't reproduce.
        """
        if self.generation >= 2:
            return None  # Sterile
        
        if not self.reproduction_ready:
            return None
        
        if self.children_produced >= 2:
            return None  # Already had max children
        
        self.children_produced += 1
        
        # Create baby
        baby = SentientSourdough(
            generation=self.generation + 1,
            name=f"{self.name} Jr."
        )
        
        self.reproduction_ready = False
        self.age_turns = 0  # Reset parent's timer
        
        return baby
    
    def get_elder_loaf_weight(self) -> int:
        """Returns weight for Elder Loaf calculation (Gen 0 = 20, Gen 1 = 10, Gen 2 = 5)"""
        weights = {0: 20, 1: 10, 2: 5}
        return weights.get(self.generation, 5)
    
    def _get_oracle_wisdom(self) -> str:
        """Returns random cryptic hint."""
        wisdoms = [
            "The Milverine walks where the pavement cracks...",
            "Kennedy answers to the hum of fluorescent lights...",
            "When the Cheese Index falls, the trolls rise...",
            "The Kia Boys fear only the roundabout...",
            "Fish Fry on Friday brings fortune, Fish Fry on Tuesday brings doom...",
            "The Tumbleweave knows your secrets...",
            "Beware the administrative assistant who smiles...",
            "The East Side holds the key, but the West Allis holds the truth...",
            "When you hear 'Ope', the way is open...",
            "The Safe House is not safe from yourself..."
        ]
        return random.choice(wisdoms)
    
    def get_status_text(self) -> str:
        """Returns formatted status for UI display."""
        gen_names = {0: "Ancient", 1: "Adolescent", 2: "Young"}
        gen_name = gen_names.get(self.generation, "Unknown")
        
        status = f"{self.name} ({gen_name} Gen {self.generation})"
        status += f"\n  Form: {self.form}"
        status += f"\n  Age: {self.age_turns} turns"
        
        if self.reproduction_ready:
            status += f"\n  STATUS: Ready to reproduce!"
        
        # Add form effect description
        effect_desc = FORM_EFFECTS.get(self.form, {}).get("description", "")
        if effect_desc:
            status += f"\n  Effect: {effect_desc}"
        
        if self.form == FORM_PARTNER:
            status += f"\n  Relationship: {FORM_EFFECTS[FORM_PARTNER]['relationship_status']}"
        
        return status


class ElderLoaf:
    """
    Created when sourdoughs merge. A massive burden.
    """
    def __init__(self, component_sourdoughs: List[SentientSourdough]):
        self.name = "The Elder Loaf"
        self.components = component_sourdoughs
        self.weight = sum(s.get_elder_loaf_weight() for s in component_sourdoughs)
        self.stickiness = float('inf')
        self.is_cursed = True
        
    def __repr__(self):
        return f"<ElderLoaf: {self.weight}lbs of cursed bread>"
    
    def get_burden_text(self) -> str:
        """Returns text describing the burden."""
        burdens = [
            f"You carry {self.weight}lbs of sentient sourdough.",
            "Your back hurts. The bread judges you.",
            "You cannot run. You cannot hide. Only bread.",
            "The Elder Loaf whispers recipes you don't want to know."
        ]
        return random.choice(burdens)


class SourdoughManager:
    """
    Manages all sourdough companions in the game.
    """
    def __init__(self):
        self.sourdoughs: List[SentientSourdough] = []
        self.elder_loaf: Optional[ElderLoaf] = None
        self.has_delivered_elder_loaf = False
        
    def add_sourdough(self, sourdough: SentientSourdough):
        """Add a new sourdough to manage."""
        self.sourdoughs.append(sourdough)
        
    def advance_turn(self) -> List[str]:
        """
        Advance all sourdoughs by one turn.
        Returns list of events that occurred.
        """
        events = []
        
        # If we have an Elder Loaf, it's heavy
        if self.elder_loaf:
            if random.random() < 0.3:
                events.append(self.elder_loaf.get_burden_text())
            return events  # Elder Loaf prevents other sourdough actions
        
        # Process each sourdough
        new_sourdoughs = []
        for sd in self.sourdoughs:
            event = sd.advance_turn()
            if event:
                events.append(event)
            
            # Check for reproduction
            baby = sd.reproduce()
            if baby:
                new_sourdoughs.append(baby)
                events.append(f"*** MITOSIS! ***\n{sd.name} has reproduced! Meet {baby.name}!")
        
        # Add new babies
        self.sourdoughs.extend(new_sourdoughs)
        
        # Check for Elder Loaf formation
        if len(self.sourdoughs) >= 5 or (len(self.sourdoughs) > 0 and self.sourdoughs[0].age_turns >= 20):
            self._form_elder_loaf()
            events.append("*** THE ELDER LOAF FORMS ***\nYour sourdoughs merge into a single massive burden!")
            events.append("You can no longer run or fast travel until you deliver it to Liam in Bay View.")
        
        return events
    
    def _form_elder_loaf(self):
        """Merge all sourdoughs into Elder Loaf."""
        self.elder_loaf = ElderLoaf(self.sourdoughs)
        self.sourdoughs = []
    
    def deliver_elder_loaf(self) -> bool:
        """
        Deliver the Elder Loaf to Liam (Bay View).
        Returns True if successful, resets the cycle.
        """
        if not self.elder_loaf:
            return False
        
        self.elder_loaf = None
        self.has_delivered_elder_loaf = True
        
        # Give player a fresh starter
        new_starter = SentientSourdough(generation=0, name="The New Starter")
        self.sourdoughs.append(new_starter)
        
        return True
    
    def get_date_night_event(self) -> Optional[str]:
        """
        Returns special event text if player has Partner form.
        Should trigger when visiting The Vanguard with Partner.
        """
        for sd in self.sourdoughs:
            if sd.form == FORM_PARTNER:
                return f"""
*** DATE NIGHT AT THE VANGUARD ***
You and {sd.name} share a Duck BLT Sausage.
The bread-being stares at you with gluten-intense eyes.
"This is nice," it bubbles.

Your Stress -20
Your confusion about your life choices +100
"""
        return None
    
    def get_puddle_slide_destination(self, current_location: str, valid_neighbors: List[str]) -> Optional[str]:
        """
        If any sourdough is in Puddle form, may slide to random neighbor.
        Returns destination or None.
        """
        for sd in self.sourdoughs:
            if sd.form == FORM_PUDDLE:
                if random.random() < FORM_EFFECTS[FORM_PUDDLE]["slide_chance"]:
                    if valid_neighbors:
                        return random.choice(valid_neighbors)
        return None
    
    def consume_food_for_homunculus(self, player_inventory: List[Any]) -> Optional[str]:
        """
        If Homunculus form exists, consumes food from inventory.
        Returns narrative text or None.
        """
        for sd in self.sourdoughs:
            if sd.form == FORM_HOMUNCULUS and sd.hunger >= 1:
                # Find food item
                for i, item in enumerate(player_inventory):
                    item_name = item.name if hasattr(item, 'name') else str(item)
                    if any(food in item_name.lower() for food in ['taco', 'rib', 'burger', 'chili', 'cheese', 'fish', 'bread', 'donut', 'coffee']):
                        player_inventory.pop(i)
                        sd.hunger = 0
                        return f"{sd.name} (The Homunculus) devours your {item_name}! It seems satisfied."
                
                # No food found - stress increases
                sd.hunger += 1
                return f"{sd.name} (The Homunculus) finds no food and GLARES at you. (+10 Stress)"
        
        return None
    
    def get_display_text(self) -> str:
        """Returns formatted text for UI display."""
        if self.elder_loaf:
            return f"THE ELDER LOAF ({self.elder_loaf.weight}lbs)\nDeliver to Liam in Bay View!"
        
        if not self.sourdoughs:
            return "No active sourdough companions."
        
        lines = []
        for sd in self.sourdoughs:
            lines.append(sd.get_status_text())
        
        return "\n---\n".join(lines)


# Global manager instance
sourdough_manager = SourdoughManager()


def acquire_starter(player_name: str) -> SentientSourdough:
    """
    Grants the player their first sourdough starter.
    Usually given by Liam or found at the Milwaukee Public Market.
    """
    starter = SentientSourdough(generation=0, name="The Starter")
    sourdough_manager.add_sourdough(starter)
    return starter
