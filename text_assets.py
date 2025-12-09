"""
text_assets.py - The Narrative Database (Agent Zeta)

This module contains only data structures (dictionaries) for flavor text,
lore, and narrative assets. No game logic is included here.

Tone: Satirical, absurd, Milwaukee-specific.
"""

CLIENT_SCENARIOS = {
    "Chloe": [
        ("Chill", "Chloe is eating pierogis while coding on a laptop from 1999."),
        ("Chill", "Chloe is in the basement trying to rewire the Basilica's bells."),
        ("Chill", "Chloe is rewiring a 1990s GameBoy."),
        ("Crisis", "Chloe accidentally hacked the Mayor's fridge and the Feds are outside."),
        ("Crisis", "Chloe's homemade server farm melted the fuse box."),
        ("Crisis", "I tried to automate my taxes and accidentally hacked the Pentagon.")
    ],
    "Bobbie": [
        ("Chill", "Bobbie is polishing his Dale Earnhardt commemorative plates."),
        ("Chill", "Bobbie is asleep in a recliner from 1985."),
        ("Chill", "Bobbie is organizing VHS tapes."),
        ("Crisis", "Bobbie is fighting a 'Demon' in his closet (it's unpaid parking tickets)."),
        ("Crisis", "Bobbie bought 400lbs of birdseed on QVC and is trapped."),
        ("Crisis", "The Demon in the Closet won't let me get my winter coat.")
    ],
    "Liam": [
        ("Chill", "Liam is waxing his mustache and listening to a band that doesn't exist yet."),
        ("Chill", "Liam offers you a deconstructed coffee. It's just beans and hot water separately."),
        ("Chill", "Liam is fermenting kim-chi in a bathtub."),
        ("Crisis", "Liam's sourdough starter has grown too large and is consuming the kitchen."),
        ("Crisis", "Liam is having a panic attack because he saw someone wearing cargo shorts."),
        ("Crisis", "My sourdough starter has gained sentience and is holding the cat hostage.")
    ],
    "Mrs. Higgins": [
        ("Chill", "Mrs. Higgins feeds you sweet potato pie until you can't move."),
        ("Chill", "Mrs. Higgins is watching her stories (Soap Operas) at max volume."),
        ("Crisis", "The City hasn't fixed the pothole in front of her house. She is ready for war."),
        ("Crisis", "Her grandson installed 'The TikTok' on her phone and she is confused."),
        ("Crisis", "The City Inspector is trying to fine her for her porch steps.")
    ],
    "Tyler": [
        ("Chill", "Tyler is playing hacky-sack. It is 2025. You are confused."),
        ("Chill", "Tyler is asleep in the library. He has drooled on a textbook."),
        ("Crisis", "Tyler has to write a 40-page thesis by tomorrow. He hasn't started."),
        ("Crisis", "Tyler forgot to pay his tuition and is about to be expelled.")
    ]
}

LANDMARK_FLAVOR = {
    "Sobelman's": "A temple of excess where a Bloody Mary comes with a whole fried chicken attached. The floor is sticky with the dreams of tourists.",
    "The Domes": "Three glass boobs rising from the mist. One is tropical, one is desert, and one is just for weddings. Half the glass panels are falling out, adding an element of danger to your botanical tour.",
    "The Art Museum": "The Calatrava wings open and close like a giant, expensive bird. It’s beautiful, until you realize it’s judging your outfit.",
    "The Safe House": "The worst-kept secret in the city. You have to dance like a chicken to get in, while tourists watch on a CCTV monitor and laugh at your lack of rhythm.",
    "Lake Michigan": "A vast, beautiful, and terrifyingly cold ocean. It beckons you to swim, but you know better. The alewives are watching.",
    "Milwaukee River": "It flows through downtown like a brown ribbon of history. Don't touch the water. Seriously. It smells like dead fish and regrets.",
    "Hoan Bridge": "The Hoan Bridge looms with its new anti-suicide fence. It's so effective that a local regular, 'Despair Dan', has given up on jumping because he 'can't figure out the damn geometry of the thing.' He now spends his Tuesday nights angrily eating pancakes at Ma Fischer's instead."
}

RANDOM_ENCOUNTERS = [
    "Tumbleweave: A weave blows past you like a western movie. It's majestic.",
    "Bridge Opening: You are stuck for 15 minutes. You contemplate jumping.",
    "Found Cheese Curd: It's on the ground, but it's still warm. Do you eat it?",
    "The Kia Boys: A car drives on the sidewalk. You lose 10 years of your life (Stress +10).",
    "Construction Season: The road is closed. It has been closed since the dawn of time. Detour.",
    "The Milverine: You see him walking. He is shirtless. He is glorious.",
    "Festival Parking: You pay $20 to park on someone's lawn.",
    "Winter Parking Ban: You parked on the wrong side. Your car is gone.",
    "You see a 'Re-Elect Tom Barrett' sticker fading on a light pole.",
    "A seagull tries to steal your hot dog. It has a knife.",
    "Someone says 'Ope' as they bump into you. You both apologize for five minutes.",
    "You smell yeast. It's either the brewery or the lake. You decide not to investigate."
]

ASCII_ART = {
    "TITLE": r"""
    .   *   ..  . *  *
   *  ~  ~  ~  ~  ~  *   .
  .  /\_/\   CASE WORKER   /\_/\  .
    ( o.o )  CREAM CITY   ( o.o )
     > ^ <   CHRONICLES    > ^ <
   *  ~  ~  ~  ~  ~  *
      .  *  .  .  *
""",
    "GAME_OVER": r"""
   ~*~*~*~*~*~*~*~*~*~*~*~*~*~
     G A M E   O V E R
   You moved to Madison.
   (It's nicer, but boring)
   ~*~*~*~*~*~*~*~*~*~*~*~*~*~
""",
    "COMBAT": r"""
      /!\  CRISIS MODE  /!\
     (ง •̀_•́)ง   FIGHT!   (ง •̀_•́)ง
""",
    "KENNEDY": r"""
       .+.   THE SORCERESS   .+.
      (o o)     KENNEDY     (o o)
       \-/   ADMIN OVERRIDE  \-/
""",
    "MILVERINE": r"""
      \m/   THE LEGEND    \m/
       |    MILVERINE      |
      / \   WALKS AMONG US / \
"""
}
