from typing import List, Dict, Any, Optional

class Item:
    """Base class for inventory items."""
    def __init__(self, name: str, description: str, value: float = 0.0):
        self.name = name
        self.description = description
        self.value = value

    def __repr__(self):
        return f"<Item: {self.name}>"

class GameState:
    """
    Persists world variables and global state.
    Tracks turn count, economy modifiers (The Vibe Index), and neighborhood states.
    """
    def __init__(self):
        self.turn_count = 0

        # The Vibe Index - Economy Modifiers
        self.global_economy_modifier = {
            "Cheese_Index": 1.0,         # Affects food prices
            "Pothole_Index": 1.0,        # Affects travel costs
            "Gentrification_Meter": 1.0  # Raises prices in specific neighborhoods
        }

        # Track local events in neighborhoods
        self.neighborhood_states: Dict[str, Dict[str, Any]] = {}

    def advance_turn(self):
        """Advances the game turn and updates world state."""
        self.turn_count += 1
        # Future logic for updating indices or triggering events can go here

    def update_economy(self, cheese_mod: float = 0.0, pothole_mod: float = 0.0, gentrification_mod: float = 0.0):
        """Updates the global economy modifiers."""
        self.global_economy_modifier["Cheese_Index"] += cheese_mod
        self.global_economy_modifier["Pothole_Index"] += pothole_mod
        self.global_economy_modifier["Gentrification_Meter"] += gentrification_mod

    def set_neighborhood_event(self, neighborhood: str, event_name: str, active: bool = True):
        """Sets an event state for a specific neighborhood."""
        if neighborhood not in self.neighborhood_states:
            self.neighborhood_states[neighborhood] = {}
        self.neighborhood_states[neighborhood][event_name] = active

    def get_neighborhood_event(self, neighborhood: str, event_name: str) -> bool:
        """Checks if a specific event is active in a neighborhood."""
        return self.neighborhood_states.get(neighborhood, {}).get(event_name, False)


class Player:
    """
    Tracks player stats including 'Billable Hours' and object-based inventory.
    """
    def __init__(self, name: str):
        self.name = name

        # Core Stats
        self.hp = 100
        self.max_hp = 100
        self.stress = 0
        self.max_stress = 100

        # Economy & Progression
        self.money = 60.00
        self.billable_hours = 0.0  # Tracks unpaid work instead of just money
        self.exp = 0

        # World State
        self.current_location = "Downtown"
        self.inventory: List[Any] = [] # Supports Object instances

        # Relationships & Status
        self.client_relationships: Dict[str, Dict[str, Any]] = {} # e.g. {'Chloe': {'trust': 10, 'cooldown': 0}}
        self.blessed_by_milverine = False

    def is_alive(self) -> bool:
        return self.hp > 0 and self.stress < self.max_stress

    def add_billable_hours(self, hours: float):
        """Adds billable hours. Satire: These are not immediately paid."""
        self.billable_hours += hours

    def add_item(self, item: Any):
        """Adds an item object to inventory."""
        self.inventory.append(item)

    def remove_item(self, item_name: str) -> bool:
        """Removes an item by name. Returns True if found and removed."""
        for i, item in enumerate(self.inventory):
            # Check if item is an object with a name attribute or just a string (for backward compatibility)
            curr_name = item.name if hasattr(item, 'name') else item
            if curr_name == item_name:
                self.inventory.pop(i)
                return True
        return False

    def has_item(self, item_name: str) -> bool:
        """Checks if player has an item by name."""
        for item in self.inventory:
            curr_name = item.name if hasattr(item, 'name') else item
            if curr_name == item_name:
                return True
        return False

    def modify_money(self, amount: float):
        self.money += amount
        # Satire: Overdraft fees exist
        if self.money < 0:
            # We don't print here to avoid side effects in logic,
            # but in the main loop this should trigger a message.
            # Ideally, the engine shouldn't print, but returns status or logs.
            # For now, we mimic the original behavior but keep it clean.
            pass

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    def relax(self, amount: int):
        self.stress = max(0, self.stress - amount)

    def update_client_relationship(self, client_name: str, trust_change: int = 0, set_cooldown: int = 0):
        """Updates relationship status and cooldowns for clients."""
        if client_name not in self.client_relationships:
            self.client_relationships[client_name] = {'trust': 0, 'cooldown': 0}

        self.client_relationships[client_name]['trust'] += trust_change
        if set_cooldown > 0:
             self.client_relationships[client_name]['cooldown'] = set_cooldown

    def decrement_cooldowns(self):
        """Reduces cooldowns for all clients by 1 (called at end of turn)."""
        for client in self.client_relationships:
            if self.client_relationships[client]['cooldown'] > 0:
                self.client_relationships[client]['cooldown'] -= 1
