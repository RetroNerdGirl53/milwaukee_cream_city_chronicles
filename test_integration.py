import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure we can import modules
sys.path.append(os.getcwd())

from engine import Player, GameState, Client
import caseworker
import economy
import combat

class TestIntegration(unittest.TestCase):

    @patch('builtins.input', side_effect=['TestWorker', '2']) # Name, Travel
    @patch('builtins.print')
    def test_game_initialization(self, mock_print, mock_input):
        # We can't easily run the full main loop because it's infinite.
        # But we can test helper functions and state setup.

        player = Player("TestWorker")
        gs = caseworker.init_game_state(player)

        # Check if roster is populated
        self.assertIsNotNone(gs.client_roster.get_client("Chloe"))
        self.assertEqual(gs.client_roster.get_client("Chloe").neighborhood, "Polonia")

        # Check enemy data retrieval
        enemy_data = caseworker.get_client_enemy_data("Chloe")
        self.assertEqual(enemy_data['name'], "Sentient Roomba")

    @patch('random.choice')
    def test_scenario_retrieval(self, mock_choice):
        # We don't need to mock choice if we are testing get_client_scenarios directly returning list
        scenarios = caseworker.get_client_scenarios("Chloe", "Chill")
        self.assertTrue(len(scenarios) > 0)
        self.assertIn("pierogis", scenarios[0] + scenarios[1] + scenarios[2]) # Basic check

    def test_combat_integration(self):
        player = Player("Fighter")
        player.stress = 0
        enemy = combat.Enemy("Test Enemy", combat.Enemy.TYPE_STONEWALLER, 20)

        # Player move
        combat.resolve_turn(player, enemy, combat.MOVE_MALICIOUS_COMPLIANCE)
        self.assertTrue(enemy.hp < 20)

    def test_economy_payout(self):
        # Test the payout logic used in caseworker
        amount = economy.calculate_payout(10)
        # It's random (chance of rejection), but should be either 150 or 75
        self.assertTrue(amount == 150.0 or amount == 75.0)

if __name__ == '__main__':
    unittest.main()
