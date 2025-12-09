import unittest
from engine import Player, GameState, Item, Client, ClientRoster

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()

    def test_initialization(self):
        self.assertEqual(self.game_state.turn_count, 0)
        self.assertEqual(self.game_state.global_economy_modifier['Cheese_Index'], 1.0)
        self.assertEqual(self.game_state.global_economy_modifier['Pothole_Index'], 1.0)
        self.assertEqual(self.game_state.neighborhood_states, {})
        self.assertIsInstance(self.game_state.client_roster, ClientRoster)

    def test_advance_turn(self):
        self.game_state.advance_turn()
        self.assertEqual(self.game_state.turn_count, 1)

    def test_update_economy(self):
        self.game_state.update_economy(cheese_mod=0.5, pothole_mod=-0.2)
        self.assertEqual(self.game_state.global_economy_modifier['Cheese_Index'], 1.5)
        self.assertEqual(self.game_state.global_economy_modifier['Pothole_Index'], 0.8)

    def test_neighborhood_events(self):
        self.game_state.set_neighborhood_event("Riverwest", "Street Festival")
        self.assertTrue(self.game_state.get_neighborhood_event("Riverwest", "Street Festival"))

class TestClientPersistence(unittest.TestCase):
    def setUp(self):
        self.roster = ClientRoster()
        self.client = Client("Chloe", "Polonia", "Chill")
        self.roster.add_client(self.client)

    def test_client_attributes(self):
        self.assertEqual(self.client.name, "Chloe")
        self.assertEqual(self.client.neighborhood, "Polonia")
        self.assertEqual(self.client.mood, "Chill")

    def test_roster_retrieval(self):
        retrieved = self.roster.get_client("Chloe")
        self.assertEqual(retrieved, self.client)
        self.assertIsNone(self.roster.get_client("Nobody"))

    def test_mood_update(self):
        self.client.set_mood("Crisis")
        self.assertEqual(self.client.mood, "Crisis")

    def test_neighborhood_query(self):
        client2 = Client("Bobbie", "West Allis", "Chill")
        self.roster.add_client(client2)
        polonia_residents = self.roster.get_clients_in_neighborhood("Polonia")
        self.assertIn(self.client, polonia_residents)
        self.assertNotIn(client2, polonia_residents)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestSubject")

    def test_initialization(self):
        self.assertEqual(self.player.name, "TestSubject")
        self.assertEqual(self.player.hp, 100)
        self.assertEqual(self.player.stress, 0)
        self.assertEqual(self.player.billable_hours, 0.0)
        self.assertEqual(self.player.inventory, [])

    def test_billable_hours(self):
        self.player.add_billable_hours(1.5)
        self.assertEqual(self.player.billable_hours, 1.5)

    def test_inventory_item_objects(self):
        item = Item("Rib Tips", "Smoky healing", 18.00, hp_restore=50)
        self.player.add_item(item)
        self.assertTrue(self.player.has_item("Rib Tips"))
        self.assertEqual(self.player.inventory[0].hp_restore, 50)

    def test_client_relationships(self):
        self.player.update_client_relationship("Chloe", trust_change=5, set_cooldown=3)
        self.assertEqual(self.player.get_client_trust("Chloe"), 5)
        self.assertEqual(self.player.get_client_cooldown("Chloe"), 3)

        self.player.decrement_cooldowns()
        self.assertEqual(self.player.get_client_cooldown("Chloe"), 2)

if __name__ == '__main__':
    unittest.main()
