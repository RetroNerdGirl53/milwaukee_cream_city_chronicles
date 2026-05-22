"""
save_system.py - Persistent State Management

Handles saving/loading game state to JSON files.
Includes crypto token generation for special collectible items.
"""

import json
import os
import hashlib
import time
from typing import Dict, Any, Optional
from pathlib import Path

SAVE_DIR = Path.home() / ".cream_city_chronicles"
SAVE_FILE = SAVE_DIR / "savegame.json"
TOKEN_FILE = SAVE_DIR / "collected_tokens.json"


def ensure_save_dir():
    """Creates save directory if it doesn't exist."""
    SAVE_DIR.mkdir(parents=True, exist_ok=True)


def generate_crypto_token(item_name: str, player_name: str, timestamp: float = None) -> str:
    """
    Generates a unique cryptographic token for special collectible items.
    This creates a "proof of ownership" hash that can be verified offline.
    
    The token is a SHA-256 hash of:
    - Item name
    - Player name  
    - Timestamp
    - A secret pepper (game-specific)
    
    This allows players to "prove" they earned rare items without a central server.
    """
    if timestamp is None:
        timestamp = time.time()
    
    # Secret pepper - game-specific constant (not secure for real crypto, but fine for game)
    PEPPER = "CreamCity414_BlessedByTheMilverine_2025"
    
    # Create unique string
    token_data = f"{item_name}:{player_name}:{timestamp}:{PEPPER}"
    
    # Generate hash
    token_hash = hashlib.sha256(token_data.encode()).hexdigest()
    
    # Format as readable token (first 16 chars)
    return {
        "item": item_name,
        "player": player_name,
        "timestamp": timestamp,
        "token_id": token_hash[:16].upper(),
        "full_hash": token_hash,
        "verified": True
    }


def verify_token(token_data: Dict[str, Any]) -> bool:
    """
    Verifies a token's authenticity offline.
    Returns True if the token is valid and untampered.
    """
    PEPPER = "CreamCity414_BlessedByTheMilverine_2025"
    
    expected_data = f"{token_data['item']}:{token_data['player']}:{token_data['timestamp']}:{PEPPER}"
    expected_hash = hashlib.sha256(expected_data.encode()).hexdigest()
    
    return expected_hash == token_data.get("full_hash", "")


class TokenRegistry:
    """
    Manages collectible cryptographic tokens for special in-game items.
    These are "NFT-like" collectibles that exist as verifiable hashes.
    """
    
    # Special items that generate tokens
    TOKEN_ITEMS = {
        "Wolski's Sticker": {
            "description": "I Survived Wolski's. The sticker is a badge of honor.",
            "rarity": "Common",
            "max_supply": 10000
        },
        "Bloody Masterpiece NFT": {
            "description": "A cryptographic proof you consumed the legendary Sobelman's Bloody Mary.",
            "rarity": "Legendary", 
            "max_supply": 1000
        },
        "Administrative Override": {
            "description": "Kennedy's blessing. A spectral rubber stamp of power.",
            "rarity": "Epic",
            "max_supply": None  # Unlimited, but requires ritual
        },
        "Milverine's Blessing": {
            "description": "Proof you were saved by the legend himself.",
            "rarity": "Mythic",
            "max_supply": 414  # Limited to area code
        },
        "Fish Fry Certificate": {
            "description": "Verified consumption of Friday Fish Fry.",
            "rarity": "Common",
            "max_supply": 50000
        },
        "Tumbleweave Slayer": {
            "description": "Proof of defeating the legendary sentient weave of Milwaukee.",
            "rarity": "Legendary",
            "max_supply": 414,
        },
        "Deep Thought Pilgrimage": {
            "description": "You visited the beached yacht SS Milwaukee energy before the city took it.",
            "rarity": "Rare",
            "max_supply": 4140,
        },
        "Survived Winter": {
            "description": "You lived through snow emergency season and still showed up to work.",
            "rarity": "Uncommon",
            "max_supply": 10000,
        },
        "Parked During Snow Emergency": {
            "description": "Your car was towed OR you somehow avoided it. Either way, you have a story.",
            "rarity": "Rare",
            "max_supply": 5000,
        },
        "Boat Removal Witness": {
            "description": "You saw Deep Thought leave on the Hoan. A era ended.",
            "rarity": "Legendary",
            "max_supply": 414,
        },
        "Pool Wall Pilgrim": {
            "description": "You witnessed the haunted Rave pool and paid respects at the wall.",
            "rarity": "Rare",
            "max_supply": 2401,
        },
        "Eagles Club Survivor": {
            "description": "You descended to the basement, met the legends, and left with your soul.",
            "rarity": "Epic",
            "max_supply": 1927,
        },
    }
    
    def __init__(self):
        ensure_save_dir()
        self.tokens: Dict[str, list] = {}
        self._load()
    
    def _load(self):
        """Load collected tokens from file."""
        if TOKEN_FILE.exists():
            try:
                with open(TOKEN_FILE, 'r') as f:
                    self.tokens = json.load(f)
            except:
                self.tokens = {}
        else:
            self.tokens = {}
    
    def _save(self):
        """Save collected tokens to file."""
        with open(TOKEN_FILE, 'w') as f:
            json.dump(self.tokens, f, indent=2)
    
    def mint_token(self, item_name: str, player_name: str) -> Optional[Dict[str, Any]]:
        """
        Mints a new token for a collectible item.
        Returns the token data if successful, None if item isn't tokenized.
        """
        if item_name not in self.TOKEN_ITEMS:
            return None
        
        # Check supply limits
        item_config = self.TOKEN_ITEMS[item_name]
        current_supply = len(self.tokens.get(item_name, []))
        max_supply = item_config.get("max_supply")
        
        if max_supply and current_supply >= max_supply:
            return None  # Max supply reached
        
        # Generate token
        token = generate_crypto_token(item_name, player_name)
        token["rarity"] = item_config["rarity"]
        token["description"] = item_config["description"]
        token["supply_number"] = current_supply + 1
        if max_supply:
            token["supply_info"] = f"#{token['supply_number']} of {max_supply}"
        else:
            token["supply_info"] = f"#{token['supply_number']}"
        
        # Store token
        if item_name not in self.tokens:
            self.tokens[item_name] = []
        self.tokens[item_name].append(token)
        self._save()
        
        return token
    
    def get_player_tokens(self, player_name: str) -> list:
        """Get all tokens owned by a specific player."""
        player_tokens = []
        for item_name, token_list in self.tokens.items():
            for token in token_list:
                if token.get("player") == player_name:
                    player_tokens.append(token)
        return player_tokens
    
    def display_collection(self, player_name: str):
        """Display a player's token collection."""
        tokens = self.get_player_tokens(player_name)
        
        if not tokens:
            print("No cryptographic collectibles yet.")
            return
        
        print("\n" + "=" * 50)
        print("   CRYPTO COLLECTION - VERIFIED TROPHIES")
        print("=" * 50)
        
        for token in tokens:
            rarity_colors = {
                "Common": "\033[37m",    # White
                "Epic": "\033[35m",      # Magenta  
                "Legendary": "\033[33m", # Yellow
                "Mythic": "\033[36m"     # Cyan
            }
            color = rarity_colors.get(token["rarity"], "\033[37m")
            reset = "\033[0m"
            
            print(f"\n{color}[{token['rarity'].upper()}]{reset}")
            print(f"  Item: {token['item']}")
            print(f"  Token ID: {token['token_id']}")
            print(f"  Supply: {token['supply_info']}")
            print(f"  {token['description']}")
            print(f"  Verified: {'✓' if verify_token(token) else '✗ CORRUPTED'}")
        
        print("\n" + "=" * 50)
        print("   These tokens are cryptographically verifiable")
        print("   offline using SHA-256 hashing.")
        print("=" * 50)


def serialize_game_state(player, game_state) -> Dict[str, Any]:
    """
    Converts player and game state to serializable dictionary.
    """
    # Serialize inventory items
    inventory_data = []
    for item in player.inventory:
        if hasattr(item, '__dict__'):
            # It's an object (Item instance)
            inventory_data.append({
                "type": "object",
                "name": item.name,
                "description": item.description,
                "value": item.value,
                "hp_restore": item.hp_restore,
                "stress_relief": item.stress_relief
            })
        else:
            # It's a string (legacy)
            inventory_data.append({
                "type": "string",
                "value": item
            })
    
    # Serialize client roster
    clients_data = {}
    for name, client in game_state.client_roster.clients.items():
        clients_data[name] = {
            "name": client.name,
            "neighborhood": client.neighborhood,
            "mood": client.mood
        }
    
    return {
        "version": "1.0",
        "timestamp": time.time(),
        "player": {
            "name": player.name,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "stress": player.stress,
            "max_stress": player.max_stress,
            "money": player.money,
            "billable_hours": player.billable_hours,
            "exp": player.exp,
            "current_location": player.current_location,
            "inventory": inventory_data,
            "client_relationships": player.client_relationships,
            "blessed_by_milverine": player.blessed_by_milverine
        },
        "game_state": {
            "turn_count": game_state.turn_count,
            "global_economy_modifier": game_state.global_economy_modifier,
            "neighborhood_states": game_state.neighborhood_states,
            "reputation_414": getattr(game_state, "reputation_414", 0),
            "quest_progress": getattr(game_state, "quest_progress", {}),
            "active_quest": getattr(game_state, "active_quest", None),
            "flags": getattr(game_state, "flags", {}),
            "clients": clients_data
        },
        "player_extra": {
            "held_item": getattr(player, "held_item", None),
            "tallboy_state": getattr(player, "tallboy_state", None),
        }
    }


def deserialize_game_state(data: Dict[str, Any]):
    """
    Converts saved data back to Player and GameState objects.
    Returns (player, game_state) tuple.
    """
    from engine import Player, GameState, Client, Item
    
    # Reconstruct player
    p_data = data["player"]
    player = Player(p_data["name"])
    player.hp = p_data["hp"]
    player.max_hp = p_data["max_hp"]
    player.stress = p_data["stress"]
    player.max_stress = p_data["max_stress"]
    player.money = p_data["money"]
    player.billable_hours = p_data["billable_hours"]
    player.exp = p_data["exp"]
    player.current_location = p_data["current_location"]
    player.client_relationships = p_data.get("client_relationships", {})
    player.blessed_by_milverine = p_data.get("blessed_by_milverine", False)
    extra = data.get("player_extra", {})
    player.held_item = extra.get("held_item")
    player.tallboy_state = extra.get("tallboy_state")
    
    # Reconstruct inventory
    player.inventory = []
    for item_data in p_data.get("inventory", []):
        if item_data.get("type") == "object":
            # Reconstruct Item object
            item = Item(
                name=item_data["name"],
                description=item_data["description"],
                value=item_data["value"],
                hp_restore=item_data["hp_restore"],
                stress_relief=item_data["stress_relief"]
            )
            player.inventory.append(item)
        else:
            # Legacy string item
            player.inventory.append(item_data["value"])
    
    # Reconstruct game state
    gs_data = data["game_state"]
    game_state = GameState()
    game_state.turn_count = gs_data["turn_count"]
    game_state.global_economy_modifier = gs_data["global_economy_modifier"]
    game_state.neighborhood_states = gs_data.get("neighborhood_states", {})
    game_state.reputation_414 = gs_data.get("reputation_414", 0)
    game_state.quest_progress = gs_data.get("quest_progress", {})
    game_state.active_quest = gs_data.get("active_quest")
    game_state.flags = gs_data.get("flags", {})
    
    # Reconstruct clients
    for name, c_data in gs_data.get("clients", {}).items():
        client = Client(
            name=c_data["name"],
            neighborhood=c_data["neighborhood"],
            mood=c_data["mood"]
        )
        game_state.client_roster.add_client(client)
    
    return player, game_state


def save_game(player, game_state, slot: str = "default") -> bool:
    """
    Saves the current game state to a JSON file.
    Returns True if successful.
    """
    try:
        ensure_save_dir()
        
        save_data = serialize_game_state(player, game_state)
        save_data["slot"] = slot
        
        save_path = SAVE_DIR / f"save_{slot}.json"
        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Save failed: {e}")
        return False


def load_game(slot: str = "default"):
    """
    Loads a game from a save slot.
    Returns (player, game_state) tuple or (None, None) if no save exists.
    """
    save_path = SAVE_DIR / f"save_{slot}.json"
    
    if not save_path.exists():
        return None, None
    
    try:
        with open(save_path, 'r') as f:
            data = json.load(f)
        
        return deserialize_game_state(data)
    except Exception as e:
        print(f"Load failed: {e}")
        return None, None


def list_save_slots() -> list:
    """Returns list of available save slots."""
    ensure_save_dir()
    slots = []
    for f in SAVE_DIR.glob("save_*.json"):
        slot_name = f.stem.replace("save_", "")
        slots.append(slot_name)
    return slots


def delete_save(slot: str = "default") -> bool:
    """Deletes a save slot. Returns True if successful."""
    save_path = SAVE_DIR / f"save_{slot}.json"
    if save_path.exists():
        save_path.unlink()
        return True
    return False


# Global token registry instance
token_registry = TokenRegistry()
