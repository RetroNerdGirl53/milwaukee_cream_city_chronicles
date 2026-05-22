"""
food_lore.py - Research-backed flavor, jokes, review parodies, and visit chatter.

Sources: Yelp/Google review themes, local press (Urban Milwaukee, JSONLine, Shepherd Express),
and Milwaukee food culture (not verbatim quotes — satirical paraphrase).
"""

import random
from typing import Dict, List, Optional

# landmark key -> lore bundle
FOOD_LORE: Dict[str, Dict] = {
    "Big Sharks (North Ave)": {
        "known_for": ["Philly cheesesteaks the size of your forearm", "late-night fish & chicken", "Nachos Supreme (DoorDash cult favorite)", "Italian beef that makes people cry after 14 years away"],
        "jokes": [
            "The dining room is 'extremely cold' per Yelp — dress like you're fishing for sharks.",
            "Someone said don't fry the sub bread. Someone else did anyway.",
            "Rami at the register is Milwaukee famous on DoorDash. You don't know Rami. You will.",
        ],
        "reviews": [
            "★★★★☆ 'Came back after 14 years — OMG they rocked my soul with onion rings and Italian beef.'",
            "★★★☆☆ 'Philly was HUGE. Fried mushrooms had no dipping sauce. Emotional damage.'",
            "★★★★★ 'Steam coming off every tender bite. Soft roll. Thank you Big Shark's.'",
        ],
    },
    "Big Sharks (Appleton)": {
        "known_for": ["Strip mall Point Plaza location", "no pizza at this one (Urban Milwaukee lore)", "same sharks, new Hampton traffic"],
        "jokes": ["Turn on the heat — patrons have filed formal requests.", "Sweet register person vs. 'extremely cold' room — pick your fighter."],
        "reviews": [
            "★★★★☆ 'Young lady at register was personable. Place clean. Heat optional.'",
            "★★★☆☆ 'Food mediocre but people were nice. 4½ stars for vibes only.'",
        ],
    },
    "Big Sharks (Teutonia)": {
        "known_for": ["North side late night", "Philly Mix (steak AND chicken)", "wings 'fresh out the fryer'"],
        "jokes": ["Teutonia Ave teaches patience. Your food teaches reward."],
        "reviews": ["★★★★★ 'Wing and fries fresh out the fryer. Yummy.'", "★★★★☆ 'Best around town. Always fresh.'"],
    },
    "JJ Fish & Chicken (35th St)": {
        "known_for": ["Open till 2am", "JJ's Snack Box", "mild sauce mythology", "the city's unofficial emergency kitchen"],
        "jokes": [
            "Five JJs on one website. Milwaukee is just JJs all the way down.",
            "You don't find JJ's. JJ's finds you at 11:47pm.",
        ],
        "reviews": [
            "★★★★★ 'Friday fish line worth it.'",
            "★★★★☆ 'Snack box saved my week.'",
        ],
    },
    "JJ Fish & Chicken (Capitol Dr)": {
        "known_for": ["Capitol Drive institution", "Friday fish fry energy on a Tuesday if you believe"],
        "jokes": ["Capitol Dr JJ is where fish and hope share a fryer."],
        "reviews": ["★★★★☆ 'Line out the door. Nobody's mad. Un-Milwaukee.'"],
    },
    "JJ Fish & Chicken (MLK Dr)": {
        "known_for": ["King Drive community spot", "slightly earlier close than 35th — plan your crisis"],
        "jokes": ["MLK Dr JJ: living room with a menu."],
        "reviews": ["★★★★☆ 'Reliable. Loud fryer. Love.'"],
    },
    "Gold Rush Chicken (Howell)": {
        "known_for": ["Brown-and-yellow siding visible from space", "buckets of chicken", "the ONLY surviving Gold Rush"],
        "jokes": [
            "Tony's on North took the old location. Gold Rush on Howell took your heart.",
            "You can still get pizza at Howell. North Ave location is a ghost with good signage.",
        ],
        "reviews": [
            "★★★★☆ 'South side bucket lunch. Generous. Napkins mandatory.'",
            "★★★★★ 'Institution. Don't question the yellow.'",
        ],
    },
    "Gold Rush Chicken (North Ave — Closed)": {
        "known_for": ["Closed 2018", "26th & North intersection landmark", "Tony's on North now", "sign still iconic"],
        "jokes": [
            "You order a Ghost Bucket. It costs $0. It tastes like memory and gentrification.",
            "Urban Milwaukee: 'eye-catching brown-and-yellow siding dominated the intersection.' It still does in your soul.",
        ],
        "reviews": [
            "★☆☆☆☆ 'Permanently closed.' — MapQuest, emotionally",
            "★★★★★ 'I remember when.' — every Milwaukeean over 30",
        ],
    },
    "Fryerz": {
        "known_for": [
            "Milwaukee's Fried Chicken Headquarters™ (self-proclaimed, earned)",
            "pizza puff + fries combo",
            "Italian beef",
            "open till 3:30am Friday/Saturday",
            "parking 'hectic' — review consensus",
        ],
        "jokes": [
            "Menupix ranked them #1765 of 2128 restaurants. Loyalists consider this a badge of honor.",
            "Milk wings are a flavor. We don't explain Milk wings.",
            "Delivery zone: 'East to the Lake, West to 90th' — Fryerz claims half the map.",
        ],
        "reviews": [
            "★★★★☆ 'Best seasoning ever.'",
            "★★★★★ 'Pizza puff with fries — 63% approval and that's science.'",
            "★★★☆☆ 'Parking hectic but worth it.'",
            "★★★★☆ 'Surprisingly pleasant kindness in this neighborhood.'",
        ],
    },
    "Mad Chicken (East North)": {
        "known_for": ["All-natural never-frozen tenders", "waffle fries", "directly across from Ian's — college Final Boss corridor"],
        "jokes": [
            "Mad Chicken and Ian's on the same block: carbs vs. protein. UWM chooses both.",
            "Cargo shorts panic attack (local lore from Bay View, but felt here too).",
        ],
        "reviews": [
            "★★★★☆ 'Real ingredients propaganda that actually tastes good.'",
            "★★★★★ 'Mad sauce on the sandwich. No frozen sermon needed.'",
        ],
    },
    "Mad Chicken (Appleton)": {
        "known_for": ["Drive-thru in old Wong's Wok", "7424 W Appleton expansion", "breakfast biscuit"],
        "jokes": ["Plumbing problems at the old Capitol site? Appleton wins. Milwaukee adapts."],
        "reviews": ["★★★★☆ 'Drive-thru tenders. Northwest side secured.'"],
    },
    "Culver's (Juneau)": {
        "known_for": ["ButterBurger", "Frozen Custard", "cheese curds that squeak", "Wisconsin state religion"],
        "jokes": [
            "Custard vs. Kopp's is Milwaukee's only holy war that ends in dessert.",
            "Concrete Mixer: custard so thick spoons file for worker's comp.",
        ],
        "reviews": [
            "★★★★★ 'Curds squeaked. I felt alive.'",
            "★★★★☆ 'Butter on the bun. Literally. Proudly.'",
        ],
    },
    "Culver's (Kinnickinnic)": {
        "known_for": ["Bay View post-bar custard", "Fish sandwich backup fish fry"],
        "jokes": ["Kinnickinnic Culver's at midnight: hoopties, hope, and mint explosion."],
        "reviews": ["★★★★☆ 'Line of cars. Worth it. Bay View classic.'"],
    },
    "Miss Katie's Diner": {
        "known_for": [
            "Presidents & politicians (Clinton + Kohl 1996, Hillary blizzard stop, Michelle Obama lunch, Trump 2016)",
            "life-size cutouts of Hillary & Michelle in dining room",
            "homemade malts — 'best in Milwaukee' (their claim, jury agrees)",
            "meatloaf with American flag toothpick",
            "RNC 'Breakfast with Friends' 2024",
            "Rachael Ray $40 a Day omelet ($7.95 now)",
        ],
        "jokes": [
            "Chili might be sugary — one Yelp warrior warned you. Order anyway.",
            "Laverne and Shirley would feel comfortable. You feel underdressed.",
            "Fox News ate here. You eat here. Democracy continues.",
        ],
        "reviews": [
            "★★★★★ 'Probably the best bacon I've ever had. Crispy. Crunchy. Spiritual.'",
            "★★★★☆ 'Dine where Michelle Obama, Clinton, and more ate. Highly recommend.'",
            "★★★☆☆ 'Chili was very sugary. Burger was really good though.'",
            "★★★★☆ 'Meatloaf so heavy I needed three waters. Flag toothpick quaint.'",
        ],
    },
    "Ma Fischer's (Brady St)": {
        "known_for": ["24 hours", "3am pancakes", "Despair Dan from Hoan Bridge fence lore", "Brady Street survival food"],
        "jokes": [
            "Open 24 hours because the city never sleeps, only stresses.",
            "Despair Dan sits in booth four. You do not ask about the fence geometry.",
        ],
        "reviews": [
            "★★★★★ '3am pancakes hit different when your caseload is due Monday.'",
            "★★★★☆ 'Coffee pot since 1998. It works. Do not ask how.'",
        ],
    },
    "Ian's Pizza (North Ave)": {
        "known_for": [
            "Mac n Cheese pizza — all-time bestseller",
            "Food Network 50-best pizza in America",
            "crème fraîche base (trust the process)",
            "open till 2:30am weekends",
            "LGBTQ+ proud space",
            "puppy chow dessert",
            "menu boards by local artists",
        ],
        "jokes": [
            "Mac n Cheese pizza: 'ridiculous in the best way' — every parent of twins.",
            "Landmark Lanes next door. Bowling + slice = Milwaukee bachelor(ette) thesis.",
            "Monthly rotating flavors — commitment issues as a business model.",
        ],
        "reviews": [
            "★★★★★ 'If you know, you know. If you don't — allow me to introduce you.'",
            "★★★★★ 'Golden, bubbly, extra cheesy. Ideal pie.' — Food Network paraphrase",
            "★★★★☆ 'Late night slice after bars. Core memory unlocked.'",
        ],
    },
    "Ian's Pizza (Juneau)": {
        "known_for": ["Deer District / Fiserv pregame slices", "downtown lunch rush"],
        "jokes": ["Bucks in six, Ian's by seven."],
        "reviews": ["★★★★☆ 'Pregame slice. Postgame slice. In-game slice if you're bold.'"],
    },
    "Pizza Shuttle (Farwell)": {
        "known_for": [
            "Since 1985 / employee-owned since 2022",
            "open till 3am (4am in reviews — Milwaukee Standard Time)",
            "Best of Milwaukee awards",
            "Winston the delivery driver (review legend)",
            "pinball + TVs",
            "post-bar floppy crust that 'hits the spot at 1am'",
            "BUFFALO WINGS 9.3 on One Bite — 'come for wings'",
        ],
        "jokes": [
            "Mark Gold sold to employees, not highest bidder. Milwaukee respect.",
            "3rd Street Market Hall location: 'be worried' per one dad — Farwell is the real one.",
            "Crust 'almost liquid' after midnight — that's not a bug, it's a feature.",
        ],
        "reviews": [
            "★★★★★ 'Pizza Shuttle never lets me down!! Winston is absolutely amazing!!'",
            "★★★☆☆ '5.3 — post bar pizza. Would be amazing at 1am. Wings 9.3 though.'",
            "★★★★☆ 'Dad took me here on bad days. Original location perfect.'",
        ],
    },
    "Pizza Shuttle (3rd St Market)": {
        "known_for": ["Avenue / 3rd Street Market Hall slice shop", "employee-owned story", "lunch crowd"],
        "jokes": ["Market Hall Shuttle vs. Farwell Shuttle: choose your fighter."],
        "reviews": ["★★★★☆ 'Hot slice at lunch. Quick. Still Shuttle DNA.'"],
    },
    "New China Buffet (27th St)": {
        "known_for": [
            "3734 S 27th — the buffet on 27th",
            "crab legs when busy",
            "styrofoam plates (review controversy)",
            "horchata at fountain",
            "3.2 stars of chaos",
            "high turnover = sometimes fresh",
        ],
        "jokes": [
            "Yelp: 'sushi tasted fishy/metallic, jaw tingled.' — survivor stories only.",
            "One star: 'metal twist tie in egg roll.' — plot twist included.",
            "Another: '9/10 would recommend' right after 'one of us got upset stomach.'",
            "Buffet rule: hunt for fresh pans. Accept the carpet.",
        ],
        "reviews": [
            "★★☆☆☆ 'Styrofoam plates. Stared down while eating. Uncomfortable.'",
            "★★★★☆ 'Busy = fresh crab legs. Peaceful even when crowded.'",
            "★★★☆☆ 'Used to be the spot growing up. Mid now. Egg rolls still worth it.'",
            "★★★★☆ '9/10 — we think the weak one was weak.'",
        ],
    },
    "George Webb's (Wells St)": {
        "known_for": [
            "Two clocks one minute apart (23:59:59 open)",
            "'Free Rabbit Lunch Tomorrow'",
            "Brewers 12-game streak free burger payoff (1987 — 168,194 burgers)",
            "2 burgers cheap",
            "Evelyn's chili recipe since 1948",
        ],
        "jokes": [
            "Two clocks: legally closed one minute per day. Spiritually open forever.",
            "George offered $10 for 1,893 pennies. Your billable hours are worth less.",
            "Late-night drunk binge-eating bastion — Milwaukee Magazine said it, not us.",
        ],
        "reviews": [
            "★★★★☆ 'Good dependable fare. Two of us under $12. Not best burger ever. Good fries.'",
            "★★★★★ 'Two clocks. Chili. History. Milwaukee.pdf.'",
        ],
    },
    "Zaffiro's": {
        "known_for": ["Thin crust since 1954", "square cut tavern pizza", "pitcher beer", "East Side old school"],
        "jokes": ["Square pizza. Round arguments.", "Iceberg salad loyalty."],
        "reviews": ["★★★★★ 'Old Milwaukee before it was a brand.'", "★★★★☆ 'Thin crust cut in squares. Correct.'"],
    },
    "Kopp's Frozen Custard (Brookfield)": {
        "known_for": ["Flavor of the day board", "Glitterati sundae", "custard civil war vs Culver's"],
        "jokes": ["Lines that mean something. Flavors that mean everything."],
        "reviews": ["★★★★★ 'Flavor of the day: hope.'"],
    },
    "Meadows Frozen Custard": {
        "known_for": ["West Allis strip-mall custard", "simple menu", "National Ave pilgrimage"],
        "jokes": [
            "No ButterBurger drama. Just custard and Midwest peace.",
            "Meadows vs Kopp's vs Culver's: the truce nobody asked for but everyone eats.",
        ],
        "reviews": [
            "★★★★★ 'Simple. Perfect. Worth the drive from anywhere.'",
            "★★★★☆ 'Old school. No glitter. Still sacred.'",
        ],
    },
}


def get_lore(landmark: str) -> Dict:
    return FOOD_LORE.get(landmark, {})


def random_chatter(landmark: str) -> Optional[str]:
    """Return a random joke, review parody, or known_for fact for UI."""
    lore = get_lore(landmark)
    if not lore:
        return None
    pool: List[str] = []
    for k in lore.get("known_for", []):
        pool.append(f"KNOWN FOR: {k}")
    pool.extend(lore.get("jokes", []))
    pool.extend(lore.get("reviews", []))
    if not pool:
        return None
    return random.choice(pool)


def build_enriched_flavor(place: Dict) -> str:
    """Base flavor + address + top known_for line."""
    key = place["landmark"]
    lore = get_lore(key)
    base = place.get("flavor", "")
    addr = place.get("address", "")
    known = lore.get("known_for", [])
    tagline = known[0] if known else ""
    parts = [base]
    if tagline and tagline not in base:
        parts.append(f"Locals say: {tagline}.")
    parts.append(f"({addr})")
    return "\n".join(parts)
