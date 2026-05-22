"""
food_places.py - Real Milwaukee restaurants with accurate addresses.

Each chain with multiple locations gets its own landmark entry (2–5 where applicable).
Menus: (price, hp_restore, stress_relief, description)
"""

from typing import Dict, List, Tuple, Any
from food_lore import build_enriched_flavor

MenuItem = Tuple[float, int, int, str]
MenuDict = Dict[str, MenuItem]

# --- shared menu templates ---
def _chicken_shack_menu(special: str) -> MenuDict:
    return {
        "2pc Fish & Fries": (8.99, 18, 5, "Friday energy any day. Tartar in a tiny cup."),
        "4pc Tender Combo": (11.99, 22, 8, "Tenders, fries, roll, and a prayer."),
        "Philly Combo": (12.99, 25, 10, "Cheese, onions, grease — the Milwaukee trinity."),
        special: (10.99, 20, 12, "House specialty. Line out the door for a reason."),
        "Large Fry": (3.99, 5, 3, "Salty. Honest. Required."),
    }


FOOD_PLACES: List[Dict[str, Any]] = [
    # --- BIG SHARKS (3) ---
    {
        "landmark": "Big Sharks (North Ave)",
        "neighborhood": "Bronzeville",
        "address": "3434 W North Ave, Milwaukee, WI 53208",
        "flavor": "Big Sharks on North Ave — where Yelp says Italian beef makes people cry after 14 years away.",
        "menu": {
            "Philly Cheesesteak (HUGE)": (14.99, 22, 10, "Janetth from Yelp: 'It was HUGE.' No dipping sauce for mushrooms optional tragedy."),
            "Italian Beef Combo": (13.99, 28, 8, "Returning home in one sandwich. Onion rings recommended."),
            "Nachos Supreme": (11.99, 18, 12, "DoorDash legend Rami approves this order."),
            "4pc Tender Combo": (11.99, 22, 8, "Steam off every bite. Soft roll. On point."),
        },
    },
    {
        "landmark": "Big Sharks (Appleton)",
        "neighborhood": "Sherman Park",
        "address": "8333 W Appleton Ave, Milwaukee, WI 53218",
        "flavor": "Second Big Sharks — Point Plaza energy near Hampton. Same sharks, new strip mall.",
        "menu": _chicken_shack_menu("Appleton Ave Fish Plate"),
    },
    {
        "landmark": "Big Sharks (Teutonia)",
        "neighborhood": "Sherman Park",
        "address": "6239 N Teutonia Ave, Milwaukee, WI 53209",
        "flavor": "North side Big Sharks. Teutonia traffic watches you eat cheese balls with dignity.",
        "menu": _chicken_shack_menu("Teutonia Tender Basket"),
    },
    # --- JJ FISH & CHICKEN (5) ---
    {
        "landmark": "JJ Fish & Chicken (35th St)",
        "neighborhood": "Bronzeville",
        "address": "1334 N 35th St, Milwaukee, WI 53208",
        "flavor": "JJ's on 35th — open till 2am. The city's mild sauce emergency room.",
        "menu": {
            "JJ's Snack Box": (9.99, 20, 10, "Feeds volunteers. Feeds soul. Feeds DeShawn's meeting."),
            "2pc Fish & Fries": (8.99, 18, 5, "Friday in your heart any day of the week."),
            "Philly Combo": (12.99, 24, 8, "Cheese, onions, grease — Milwaukee Trinity."),
            "4pc Tender Combo": (11.99, 22, 8, "Line out the door for a reason."),
        },
    },
    {
        "landmark": "JJ Fish & Chicken (35th St II)",
        "neighborhood": "Washington Heights",
        "address": "3057 N 35th St, Milwaukee, WI 53210",
        "flavor": "Another JJ on 35th — different store number, same late-night salvation.",
        "menu": _chicken_shack_menu("35th Street Combo"),
    },
    {
        "landmark": "JJ Fish & Chicken (Capitol Dr)",
        "neighborhood": "Harambee",
        "address": "1955 W Capitol Dr, Milwaukee, WI 53206",
        "flavor": "Capitol Drive JJ. Friday fish line wraps the building. Worth it.",
        "menu": {
            "Capitol Fish Fry": (11.99, 26, 8, "Community Friday energy on Capitol."),
            "JJ's Snack Box": (9.99, 20, 10, "Second stop on the Mild Sauce Run."),
            "Philly Combo": (12.99, 24, 8, "For when fish isn't enough."),
        },
    },
    {
        "landmark": "JJ Fish & Chicken (MLK Dr)",
        "neighborhood": "Harambee",
        "address": "2410 N Dr. Martin Luther King Jr. Dr, Milwaukee, WI 53212",
        "flavor": "JJ on King Drive. Community living room with a fryer.",
        "menu": _chicken_shack_menu("King Drive Dinner"),
    },
    {
        "landmark": "JJ Fish & Chicken (62nd & Capitol)",
        "neighborhood": "Washington Heights",
        "address": "6212 W Capitol Dr, Milwaukee, WI 53216",
        "flavor": "West Capitol JJ — open late, smells like victory and vegetable oil.",
        "menu": _chicken_shack_menu("62nd Street Plate"),
    },
    # --- GOLD RUSH ---
    {
        "landmark": "Gold Rush Chicken (Howell)",
        "neighborhood": "Walker's Point",
        "address": "3500 S Howell Ave, Milwaukee, WI 53207",
        "flavor": "The surviving Gold Rush — brown-and-yellow siding, buckets of chicken, Milwaukee south side institution.",
        "menu": {
            "Chicken Bucket": (14.99, 30, 10, "Bucket lunch. Generous. Napkins mandatory."),
            "Fish Dinner": (13.99, 25, 8, "Friday spirit on Howell Ave."),
            "Pizza Slice": (3.50, 8, 5, "They still do pizza here. Don't question it."),
            "Ice Cream Cup": (2.99, 5, 15, "Dessert after grease. Balance."),
        },
    },
    {
        "landmark": "Gold Rush Chicken (North Ave — Closed)",
        "neighborhood": "Bronzeville",
        "address": "2625 W North Ave, Milwaukee, WI 53205 (closed since 2018)",
        "flavor": "The old Gold Rush on North & 26th. Closed but the sign still haunts the intersection. Tony's on North moved in. You feel history.",
        "menu": {
            "Ghost Bucket": (0.00, 0, 5, "You cannot order. You can remember. The siding is still yellow in your heart."),
        },
    },
    # --- FRYERZ ---
    {
        "landmark": "Fryerz",
        "neighborhood": "Amani",
        "address": "2651 W Fond du Lac Ave, Milwaukee, WI 53206",
        "flavor": "Fryerz — 'Milwaukee's Fried Chicken Headquarters.' Open till 2am. Italian beef, pizza puffs, lemon pepper wings.",
        "menu": {
            "6pc Buffalo Boneless": (12.99, 20, 8, "Fries, coleslaw, roll, regret optional."),
            "Italian Beef": (10.99, 22, 5, "Wet or dry. Hot peppers. Milwaukee baptism."),
            "Pizza Puff": (5.99, 12, 3, "A Milwaukee icon in fried pastry form."),
            "Fryerz Burger": (8.99, 18, 6, "Fresh patty. Not pretending to be healthy."),
        },
    },
    # --- MAD CHICKEN (2) ---
    {
        "landmark": "Mad Chicken (East North)",
        "neighborhood": "East Side",
        "address": "2045 E North Ave, Milwaukee, WI 53202",
        "flavor": "Mad Chicken east side — all-natural tenders, waffle fries, across from Ian's. UWM fuel.",
        "menu": {
            "Mad Chicken Sandwich": (10.99, 22, 10, "Half-pound tenders. Mad sauce. No frozen chicken sermon."),
            "Waffle Fries": (4.99, 8, 8, "Crispy lattice of happiness."),
            "4pc Tenders": (7.99, 18, 6, "Real ingredients propaganda that tastes good."),
        },
    },
    {
        "landmark": "Mad Chicken (Appleton)",
        "neighborhood": "Sherman Park",
        "address": "7424 W Appleton Ave, Milwaukee, WI 53218",
        "flavor": "Northwest Mad Chicken in the old Wong's Wok space. Drive-thru. City expanding one tender at a time.",
        "menu": {
            "Chicken Biscuit": (4.99, 12, 5, "Breakfast of case workers who gave up."),
            "Mad Fire Sandwich": (10.99, 20, 12, "Spicy mad sauce. East side energy on Appleton."),
            "6pc Tenders": (11.99, 24, 8, "Family size. No family required."),
        },
    },
    # --- CULVER'S (4) ---
    {
        "landmark": "Culver's (Juneau)",
        "neighborhood": "Downtown",
        "address": "1243 N 10th St, Milwaukee, WI 53205",
        "flavor": "Culver's ButterBurger energy downtown. Wisconsin's unofficial state religion: custard and curds.",
        "menu": {
            "ButterBurger Single": (6.49, 15, 5, "Butter on the bun. Literally. Proudly."),
            "Concrete Mixer": (4.99, 8, 18, "Custard so thick it defies spoons."),
            "Cheese Curds": (4.29, 10, 8, "Squeak. Squeak. Happiness."),
        },
    },
    {
        "landmark": "Culver's (Kinnickinnic)",
        "neighborhood": "Bay View",
        "address": "2800 S Kinnickinnic Ave, Milwaukee, WI 53207",
        "flavor": "Bay View Culver's. Post-bar custard pilgrimages. Line of hoopties at midnight.",
        "menu": {
            "Double ButterBurger": (8.49, 22, 3, "You will need a nap. You will not take one."),
            "Fish Sandwich": (6.99, 18, 5, "Friday backup plan when fish fry lines are too long."),
            "Mint Explosion Concrete": (5.49, 6, 20, "Dental work can wait."),
        },
    },
    {
        "landmark": "Culver's (Capitol)",
        "neighborhood": "Wauwatosa",
        "address": "12401 W Capitol Dr, Brookfield/Milwaukee, WI 53224",
        "flavor": "Suburban Culver's on Capitol. Minivans. Custard. The American Midwest in a cup.",
        "menu": {
            "ButterBurger Deluxe": (7.49, 20, 4, "Lettuce for plausible deniability."),
            "Family Basket": (15.99, 35, 5, "Feeds four or one very stressed social worker."),
            "Vanilla Custard Dish": (3.99, 5, 15, "Soft serve theology."),
        },
    },
    {
        "landmark": "Culver's (Howell)",
        "neighborhood": "Walker's Point",
        "address": "1634 W Howard Ave, Milwaukee, WI 53221",
        "flavor": "South side Culver's near Howell. Drive-thru diplomacy. Curd diplomacy.",
        "menu": {
            "Wisconsin Swiss Melt": (7.29, 18, 6, "Cheese on cheese. Wisconsin.pdf."),
            "Chili Cheese Curds": (5.49, 12, 4, "Spicy. Salty. Worth the antacid."),
            "Root Beer Float": (3.49, 8, 12, "Foam mustache. Dignity optional."),
        },
    },
    # --- MISS KATIE'S ---
    {
        "landmark": "Miss Katie's Diner",
        "neighborhood": "Near West Side",
        "address": "1900 W Clybourn St, Milwaukee, WI 53233",
        "flavor": "Miss Katie's — Clinton & Kohl ate here in '96. Cutouts of Hillary & Michelle watch you order.",
        "menu": {
            "Homemade Malt": (5.99, 8, 25, "Best in Milwaukee — they claim it, reviews agree. Required for political quests."),
            "Meatloaf Blue Plate": (14.99, 35, 5, "American flag toothpick included. Three waters recommended."),
            "Corned Beef Hash": (12.99, 25, 8, "Best corned beef hash — also their claim. Also fair."),
            "Rachael Ray Omelet": (7.95, 18, 10, "$40 a Day fame. Still under eight bucks."),
            "Grab & Go Bagel": (8.00, 15, 3, "Egg, meat, cheese, hash brown. Marquette speed run."),
        },
    },
    # --- MA FISCHER'S (Brady — canonical 24hr) ---
    {
        "landmark": "Ma Fischer's (Brady St)",
        "neighborhood": "Brady Street",
        "address": "1212 E Brady St, Milwaukee, WI 53202",
        "flavor": "Ma Fischer's on Brady — 24 hours. Pancakes at 3am. Despair Dan energy. The Hoan Bridge fence sent him here.",
        "menu": {
            "3am Pancakes": (6.00, 15, 10, "Despair Dan nods from booth four."),
            "Coffee Refill": (1.50, 0, 5, "The pot has been on since the Clinton administration."),
            "Friday Fish Fry": (13.00, 25, 8, "Fish fry at 2am hits different."),
        },
    },
    # --- IAN'S PIZZA (3) ---
    {
        "landmark": "Ian's Pizza (North Ave)",
        "neighborhood": "East Side",
        "address": "2035 E North Ave, Milwaukee, WI 53202",
        "flavor": "Ian's North Ave — Mac n Cheese pizza made Food Network's 50-best list. Open till 2:30am.",
        "menu": {
            "Mac n Cheese Slice": (5.50, 15, 12, "All-time bestseller. Crème sauce, mac noodles, cheddar. Thesis fuel."),
            "Mac n Cheese Slice (2nd)": (5.50, 15, 12, "Tyler needs two. You need two. Wisconsin needs two."),
            "Smokey the Bandit Slice": (5.00, 12, 8, "BBQ chicken. Name is a journey."),
            "Puppy Chow Cup": (4.00, 5, 15, "Dessert. Midwest munchie insurance."),
        },
    },
    {
        "landmark": "Ian's Pizza (Juneau)",
        "neighborhood": "Downtown",
        "address": "146 E Juneau Ave, Milwaukee, WI 53203",
        "flavor": "Downtown Ian's near the Deer District. Pre-game slices. Post-game slices. Always slices.",
        "menu": {
            "Tomato Pesto Slice": (5.50, 14, 10, "Veg-forward but still Wisconsin portion."),
            "Create Your Own Slice": (6.00, 16, 8, "Artist's choice behind the counter."),
            "Garlic Bread Sticks": (4.00, 8, 5, "Carbs before carbs."),
        },
    },
    {
        "landmark": "Ian's Pizza (Story Hill)",
        "neighborhood": "Wauwatosa",
        "address": "5300 W Bluemound Rd, Milwaukee, WI 53208",
        "flavor": "Story Hill Ian's on Bluemound. West side pizza lab. Delivery to the whole west end.",
        "menu": {
            "All the Veg Slice": (5.50, 12, 12, "Greens on pizza. Still delicious."),
            "Chicken BBQ Slice": (5.00, 14, 8, "Classic Ian's comfort."),
            "Whole Pie To Go": (22.00, 30, 15, "Feed the block club meeting."),
        },
    },
    # --- PIZZA SHUTTLE (2) ---
    {
        "landmark": "Pizza Shuttle (Farwell)",
        "neighborhood": "Brady Street",
        "address": "1827 N Farwell Ave, Milwaukee, WI 53202",
        "flavor": "Pizza Shuttle since 1985 — employee-owned, open till 3am (4am in the soul). Winston the driver is legend.",
        "menu": {
            "CYO Medium Pizza": (14.99, 25, 10, "Post-bar floppy crust — feature not bug."),
            "Soft Breadsticks": (6.99, 10, 12, "Mrs. Higgins approved."),
            "Buffalo Wings": (12.99, 20, 15, "One Bite rated 9.3. Come for wings, stay for Shuttle."),
            "Philly Cheesesteak": (10.99, 20, 8, "Not pizza. Still shuttling."),
        },
    },
    {
        "landmark": "Pizza Shuttle (3rd St Market)",
        "neighborhood": "Downtown",
        "address": "275 W Wisconsin Ave (3rd Street Market Hall), Milwaukee, WI 53203",
        "flavor": "Pizza Shuttle slice shop in the Avenue / Market Hall. Downtown lunch rush. Same legend, new food hall fit.",
        "menu": {
            "Hot Slice": (4.50, 12, 8, "By the slice. Quick. Sacred."),
            "Whole Shuttle Pie": (18.99, 28, 12, "Feed the office. Regret nothing."),
            "Southern BBQ Pizza": (16.99, 22, 10, "Award-winning menu item energy."),
        },
    },
    # --- NEW CHINA BUFFET ---
    {
        "landmark": "New China Buffet (27th St)",
        "neighborhood": "Mitchell Street",
        "address": "3734 S 27th St, Milwaukee, WI 53221",
        "flavor": "New China Buffet on 27th — styrofoam plates, crab legs when busy, Yelp chaos at 3.2 stars.",
        "menu": {
            "Lunch Buffet": (12.99, 35, 5, "Hunt fresh pans. Ignore sushi if wise."),
            "Dinner Buffet": (15.99, 40, 3, "Horchata included. Metal-free egg rolls not guaranteed."),
            "Crab Legs Plate": (0.00, 25, 10, "When busy, worth the stare-down from strangers."),
        },
    },
    # --- OTHER MILWAUKEE STAPLES ---
    {
        "landmark": "Kopp's Frozen Custard (Brookfield)",
        "neighborhood": "Wauwatosa",
        "address": "14120 W Greenfield Ave, Brookfield, WI 53214",
        "flavor": "Kopp's — the other custard church. Flavor of the day board. Lines that mean something.",
        "menu": {
            "Single Scoop": (3.50, 6, 18, "Flavor of the day: existential hope."),
            "Double Scoop": (5.00, 8, 22, "You deserve this. Probably."),
            "Glitterati Sundae": (6.50, 10, 20, "Sprinkles as personality."),
        },
    },
    {
        "landmark": "George Webb's (Wells St)",
        "neighborhood": "Downtown",
        "address": "1617 W Wells St, Milwaukee, WI 53233",
        "flavor": "George Webb's — 24 hours. Two burgers for $3 energy. The clock logo watches you.",
        "menu": {
            "2 Burgers": (3.00, 12, 0, "Famous deal. Grease included."),
            "Chili Bowl": (2.99, 10, 2, "3am survival tool."),
            "Hash Browns": (2.49, 8, 0, "Crispy budget therapy."),
        },
    },
    {
        "landmark": "George Webb's (East Side)",
        "neighborhood": "East Side",
        "address": "752 N Jefferson St, Milwaukee, WI 53202",
        "flavor": "East side George Webb's. Bar closeout fuel. The grill never sleeps.",
        "menu": {
            "2 Burgers": (3.00, 12, 0, "Same deal. Different drunk crowd."),
            "Eggs & Toast": (4.99, 14, 5, "Breakfast that knows your secrets."),
        },
    },
    {
        "landmark": "Zaffiro's Pizza",
        "neighborhood": "East Side",
        "address": "1724 N Farwell Ave, Milwaukee, WI 53202",
        "flavor": "Zaffiro's since 1954. Thin crust. Taverna vibes. Old Milwaukee before it was a brand.",
        "menu": {
            "Thin Crust Cheese": (12.00, 20, 10, "Cut in squares. Argue about it."),
            "Italian Salad": (8.50, 10, 8, "Iceberg loyalty."),
            "Pitcher of Beer": (12.00, -3, 25, "It's a tavern. Act accordingly."),
        },
    },
    {
        "landmark": "Meadows Frozen Custard",
        "neighborhood": "West Allis",
        "address": "7900 W National Ave, West Allis, WI 53214",
        "flavor": "Meadows on National Ave. West Allis custard pilgrimage. Simple. Perfect. Strip mall sacred.",
        "menu": {
            "Chocolate Custard": (3.25, 6, 16, "Classic. No pretense."),
            "Turtle Sundae": (5.75, 8, 20, "Caramel, nuts, joy."),
        },
    },
]


def build_food_menus() -> MenuDict:
    """Flat dict for landmark_menus merge."""
    out: MenuDict = {}
    for place in FOOD_PLACES:
        out[place["landmark"]] = place["menu"]
    return out


def build_food_flavor() -> Dict[str, str]:
    out = {}
    for place in FOOD_PLACES:
        out[place["landmark"]] = build_enriched_flavor(place)
    return out


def register_food_landmarks(milwaukee_map: Dict) -> None:
    """Append food landmarks to neighborhood landmark lists."""
    for place in FOOD_PLACES:
        hood = place["neighborhood"]
        key = place["landmark"]
        if hood not in milwaukee_map:
            continue
        node = milwaukee_map[hood]
        lm = node.get("landmark")
        if lm is None:
            node["landmark"] = key
        elif isinstance(lm, str):
            if lm != key:
                node["landmark"] = [lm, key]
        elif isinstance(lm, list):
            if key not in lm:
                lm.append(key)
        else:
            node["landmark"] = [key]


FOOD_MENUS: MenuDict = build_food_menus()
FOOD_FLAVOR: Dict[str, str] = build_food_flavor()

# Register on import
from world_data import MILWAUKEE_MAP
register_food_landmarks(MILWAUKEE_MAP)
