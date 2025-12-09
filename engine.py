from typing import List, Dict, Any, Optional
import random

class Item:
    """
    Base class for inventory items.
    Supports properties defined in devdoc.txt (HP/Stress effects).
    """
    def __init__(self, name: str, description: str, value: float = 0.0, hp_restore: int = 0, stress_relief: int = 0):
        self.name = name
        self.description = description
        self.value = value
        self.hp_restore = hp_restore
        self.stress_relief = stress_relief

    def __repr__(self):
        return f"<Item: {self.name} (Value: ${self.value})>"

class Client:
    """
    Represents a client in the game.
    Tracks persistent state like mood (Chill/Crisis) as per TODO 1.3.
    """
    def __init__(self, name: str, neighborhood: str, mood: str = "Chill"):
        self.name = name
        self.neighborhood = neighborhood
        self.mood = mood # "Chill" or "Crisis"

    def set_mood(self, mood: str):
        if mood in ["Chill", "Crisis"]:
            self.mood = mood

class ClientRoster:
    """
    Manages the list of clients and their states.
    TODO 1.3: Saves state between visits.
    """
    def __init__(self):
        self.clients: Dict[str, Client] = {}

    def add_client(self, client: Client):
        self.clients[client.name] = client

    def get_client(self, name: str) -> Optional[Client]:
        return self.clients.get(name)

    def get_clients_in_neighborhood(self, neighborhood: str) -> List[Client]:
        return [c for c in self.clients.values() if c.neighborhood == neighborhood]

class GameState:
    """
    Persists world variables and global state.
    Tracks turn count, economy modifiers (The Vibe Index), neighborhood states, and the Client Roster.
    TODO 1.1: Central GameState object.
    """
    def __init__(self):
        self.turn_count = 0

        # TODO 2.3: The Vibe Index - Economy Modifiers
        self.global_economy_modifier = {
            "Cheese_Index": 1.0,         # Affects food prices
            "Pothole_Index": 1.0,        # Affects travel costs
            "Gentrification_Meter": 1.0  # Raises prices in specific neighborhoods
        }

        # Track local events in neighborhoods (TODO 1.1)
        self.neighborhood_states: Dict[str, Dict[str, Any]] = {}

        # TODO 1.3: Client Persistence
        self.client_roster = ClientRoster()

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
    TODO 1.2: Stateful Player Class.
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
        self.billable_hours = 0.0  # TODO 1.2: Track unpaid work
        self.exp = 0

        # World State
        self.current_location = "Downtown"
        self.inventory: List[Any] = [] # TODO 1.2: Support Object instances

        # Relationships & Status
        # TODO 1.2: Track cooldowns and relationship levels per client
        self.client_relationships: Dict[str, Dict[str, Any]] = {}

        self.blessed_by_milverine = False # Lore integration

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
            pass # Handling logic would be in game loop/controller

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

    def get_client_cooldown(self, client_name: str) -> int:
        """Returns the current cooldown for a client."""
        return self.client_relationships.get(client_name, {}).get('cooldown', 0)

    def get_client_trust(self, client_name: str) -> int:
        """Returns the current trust level for a client."""
        return self.client_relationships.get(client_name, {}).get('trust', 0)
