import random
import time

def check_milverine_intervention(player):
    """
    Checks if the Player needs saving (HP <= 0 or Stress >= 100).
    5% chance The Milverine intervenes.
    Also triggers if the player has the 'blessed_by_milverine' flag set (legacy support).
    """
    # Check trigger conditions
    if player.hp <= 0 or player.stress >= player.max_stress:

        # Determine success: 5% chance OR pre-existing blessing
        is_blessed = getattr(player, 'blessed_by_milverine', False)
        roll = random.randint(1, 100)
        success = (roll <= 5) or is_blessed

        if success:
            print("\n" + "!"*50)
            print("THE MILVERINE INTERVENES.")
            print("The clouds part. A brisk walker approaches. He is shirtless. He is glorious.")
            print("He does not stop for the red light; the red light stops for him.")
            print("He power-walks past you, absorbing your burnout into his aura.")
            print("You are healed. He does not break stride.")
            print("!"*50)

            # Full Heal
            player.hp = player.max_hp
            player.stress = 0

            # Remove blessing if used
            if is_blessed:
                player.blessed_by_milverine = False

            return True

    return False

def summon_kennedy(player):
    """
    Attempts to summon Kennedy, the Sorceress of the System.
    Requires 'Ancient Coffee' and 'Forbidden Form 1040-X'.
    Adds 'Administrative Override' to inventory if successful.
    """
    required_items = ["Ancient Coffee", "Forbidden Form 1040-X"]

    # Check if player has items
    has_items = all(item in player.inventory for item in required_items)

    if has_items:
        print("\n...You arrange the Ancient Coffee and the Forbidden Forms...")
        print("You chant the three sacred words: 'PER. MY. EMAIL.'")
        time.sleep(2)

        print("\n" + "~"*50)
        print("THE REALITY TEARS OPEN.")
        print("Kennedy appears. She has six arms: two typing, two holding phones, two shrugging.")
        print("She floats above the desk, illuminated by the hum of fluorescent lights.")
        print("'Per my last email,' she chants, and reality bends.")
        print("~"*50)

        # Remove items
        for item in required_items:
            if item in player.inventory:
                player.inventory.remove(item)

        # Add reward
        print("\nKennedy stamps your forehead. You acquired: [Administrative Override].")
        player.inventory.append("Administrative Override")
        print("She vanishes into a cloud of toner.")
        return True
    else:
        print("\nYou lack the required ritual components (Ancient Coffee, Form 1040-X).")
        print("Nothing happens. You look foolish.")
        return False

def invoke_freeway(player):
    """
    Encounters Freeway, the Milwaukee Legend.
    Boosts morale (Stress relief).
    """
    print("\n" + "*"*40)
    print("A LEGEND APPEARS!")
    print("It's Freeway! He is wearing every piece of Bucks gear simultaneously.")
    print("He smiles and points at you with unshakeable confidence.")
    print("'YOU'RE A WINNER! MILWAUKEE IN SIX!'")
    print("His unbridled optimism is infectious.")
    print("*"*40)

    heal_stress = 20
    # Use the player's method if available, otherwise fallback to manual
    if hasattr(player, 'relax'):
        player.relax(heal_stress)
    else:
        player.stress = max(0, player.stress - heal_stress)
    print(f"Your Stress decreases by {heal_stress}. You feel like a Champion.")
