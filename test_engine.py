import unittest
from engine import Player, GameState, Item

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()

    def test_initialization(self):
        self.assertEqual(self.game_state.turn_count, 0)
        self.assertEqual(self.game_state.global_economy_modifier['Cheese_Index'], 1.0)
        self.assertEqual(self.game_state.global_economy_modifier['Pothole_Index'], 1.0)
        self.assertEqual(self.game_state.neighborhood_states, {})

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
        self.assertFalse(self.game_state.get_neighborhood_event("Riverwest", "NonExistentEvent"))
        self.assertFalse(self.game_state.get_neighborhood_event("Downtown", "Street Festival"))


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
        self.player.add_billable_hours(2.0)
        self.assertEqual(self.player.billable_hours, 3.5)

    def test_inventory_objects(self):
        item = Item("Ancient Coffee", "Black as the void", 5.00)
        self.player.add_item(item)
        self.assertTrue(self.player.has_item("Ancient Coffee"))
        self.assertEqual(self.player.inventory[0], item)

        self.player.remove_item("Ancient Coffee")
        self.assertFalse(self.player.has_item("Ancient Coffee"))
        self.assertEqual(len(self.player.inventory), 0)

    def test_inventory_strings_compatibility(self):
        # Ensure it still works with strings if needed (though we prefer objects now)
        self.player.add_item("String Item")
        self.assertTrue(self.player.has_item("String Item"))
        self.player.remove_item("String Item")
        self.assertFalse(self.player.has_item("String Item"))

    def test_client_relationships(self):
        self.player.update_client_relationship("Chloe", trust_change=5, set_cooldown=3)
        self.assertEqual(self.player.client_relationships["Chloe"]['trust'], 5)
        self.assertEqual(self.player.client_relationships["Chloe"]['cooldown'], 3)

        self.player.decrement_cooldowns()
        self.assertEqual(self.player.client_relationships["Chloe"]['cooldown'], 2)

    def test_stats_modification(self):
        self.player.heal(-10) # Damage
        self.assertEqual(self.player.hp, 90)
        self.player.heal(20) # Overheal check
        self.assertEqual(self.player.hp, 100)

        self.player.relax(-10) # Add stress (negative relax is stress? No, relax reduces stress)
        # Logic in method: self.stress = max(0, self.stress - amount)
        # So relax(10) reduces stress by 10.

        self.player.stress = 50
        self.player.relax(10)
        self.assertEqual(self.player.stress, 40)
        self.player.relax(100)
        self.assertEqual(self.player.stress, 0)

if __name__ == '__main__':
    unittest.main()
