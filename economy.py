import random

# Global Economic Indicators
CHEESE_INDEX = 1.0       # Affects food prices
POTHOLE_INDEX = 1.0      # Affects car travel costs/stress
GENTRIFICATION_METER = 1.0 # Affects rent/coffee prices

def update_market_vibes():
    """
    Randomizes global variables: 'Cheese Index', 'Pothole Index', and 'Gentrification Meter'.
    """
    global CHEESE_INDEX, POTHOLE_INDEX, GENTRIFICATION_METER

    # Randomize indices (arbitrary ranges based on "vibes")
    CHEESE_INDEX = round(random.uniform(0.8, 1.5), 2)
    POTHOLE_INDEX = round(random.uniform(0.5, 2.0), 2)
    GENTRIFICATION_METER = round(random.uniform(0.9, 1.8), 2)

    print(f"\n--- MARKET UPDATE ---")
    print(f"Cheese Index: {CHEESE_INDEX}")
    print(f"Pothole Index: {POTHOLE_INDEX}")
    print(f"Gentrification Meter: {GENTRIFICATION_METER}")
    print(f"---------------------")

def calculate_payout(billable_hours):
    """
    Calculates payout for 'The Center'.
    Converts hours to cash ($15/hr base).
    20% chance of 'Bureaucratic Rejection' where the player only gets half pay.
    """
    base_rate = 15.0
    total_pay = billable_hours * base_rate

    # 20% chance of rejection
    if random.random() < 0.20:
        print("\n*** BUREAUCRATIC REJECTION ***")
        print("Payroll found a formatting error (you used the wrong font size).")
        print("Penalty: 50% pay deduction.")
        total_pay *= 0.5

    return round(total_pay, 2)

class FoodTruck:
    """
    A Food Truck with dynamic pricing that fluctuates based on a random 'Hype' multiplier.
    """
    def __init__(self, name, base_menu):
        self.name = name
        self.base_menu = base_menu # Dictionary of item: base_price
        self.hype = 1.0
        self.update_hype()

    def update_hype(self):
        """Randomizes the Hype multiplier."""
        # Hype can swing wildly from "nobody cares" (0.5) to "viral sensation" (3.0)
        self.hype = round(random.uniform(0.5, 3.0), 2)

    def get_menu(self):
        """Returns the menu with current hype-adjusted prices."""
        adjusted_menu = {}
        for item, price in self.base_menu.items():
            # Price affected by Hype and arguably Gentrification Meter if we wanted to link them,
            # but requirements just say 'Hype' multiplier.
            adjusted_price = round(price * self.hype, 2)
            adjusted_menu[item] = adjusted_price
        return adjusted_menu

    def display_menu(self):
        print(f"\n--- {self.name} (Hype Level: {self.hype}x) ---")
        menu = self.get_menu()
        for i, (item, price) in enumerate(menu.items()):
            print(f"{i+1}. {item} - ${price}")
        return list(menu.items())
