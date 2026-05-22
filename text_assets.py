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
        ("Chill", "Chloe is writing a game for a 1990s GameBoy."),
        ("Crisis", "Chloe accidentally hacked the Mayor's fridge and the Feds are outside."),
        ("Crisis", "Chloe's homemade server farm melted the fuse box."),
        ("Crisis", "I was modding my roomba and now it's a drunk, sentient vacuum.")
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
        ("Chill", "Tyler has floor tickets to a sold-out Rave show. He's been to 14 shows there. He says the pool 'feels sad.'"),
        ("Crisis", "Tyler has to write a 40-page thesis by tomorrow. He hasn't started."),
        ("Crisis", "Tyler forgot to pay his tuition and is about to be expelled."),
        ("Crisis", "Tyler got separated from his friends in The Rave basement. He swears the pool lights turned on by themselves."),
    ],
    "DeShawn": [
        ("Chill", "DeShawn is organizing a tenant meeting with coffee and clipboards."),
        ("Chill", "DeShawn is fixing someone's porch steps because the city won't."),
        ("Chill", "DeShawn says 'We don't call the cops, we call each other.' You nod solemnly."),
        ("Crisis", "The landlord changed the locks while DeShawn was at work."),
        ("Crisis", "A slumlord sent a fake eviction notice printed on Kinko's paper."),
        ("Crisis", "The building has no heat. It's November. In Wisconsin.")
    ],
    "Grandma Roz": [
        ("Chill", "Grandma Roz pours you a whiskey and calls you 'hon'."),
        ("Chill", "Grandma Roz is yelling at the Packers on a TV from 2003."),
        ("Chill", "She knows your business before you sit down. You accept this."),
        ("Crisis", "A new bar owner wants to shut down her patio at 9pm. War."),
        ("Crisis", "Someone tagged her mural. She has a bat and a smile."),
        ("Crisis", "The health inspector is here about 'grandma's secret ingredient' (love).")
    ],
    "Mikey": [
        ("Chill", "Mikey is perfecting elote seasoning. Your mouth waters."),
        ("Chill", "Mikey's cousin is sleeping in the cart again. Family business."),
        ("Chill", "Mikey offers you corn with too much chili. You accept."),
        ("Crisis", "A rival elote cart parked on his corner. This is personal."),
        ("Crisis", "Mikey's license got 'lost' at City Hall. Again."),
        ("Crisis", "Someone called 311 about 'suspicious deliciousness.'")
    ],
    "Pastor Dale": [
        ("Chill", "Pastor Dale is counting fish fry fish with military precision."),
        ("Chill", "Pastor Dale is rehearsing a sermon about potholes (it's theological)."),
        ("Chill", "The church basement smells like heaven and grease."),
        ("Crisis", "The fryer died mid-service. Friday is in 6 hours."),
        ("Crisis", "A parishioner donated 'mystery fish' from a questionable source."),
        ("Crisis", "The health department wants paperwork for 'faith-based batter.'")
    ],
    "Jen": [
        ("Chill", "Jen went to visit the abandoned boat again. She says it's 'team building.'"),
        ("Chill", "Jen is vaping on a loading dock, staring at yachts."),
        ("Chill", "Jen swapped her nametag to say 'Not Your Concierge.'"),
        ("Chill", "Jen tells you which bathroom is actually clean. This is gold."),
        ("Crisis", "A billionaire asked her to 'smile more.' She is one HR complaint from glory."),
        ("Crisis", "Jen's tips were stolen by a manager named Chad."),
        ("Crisis", "She has to cater a yacht party for people who say 'Mil-wah-kee.'")
    ],
}

# Trust-gated hangout lines (trust >= 5)
CLIENT_DEEP_TALK = {
    "Chloe": "Chloe admits the Roomba is her emotional support appliance. You don't judge.",
    "Bobbie": "Bobbie tells you the Ticket Demon is actually his ex-wife's parking tickets from 2004.",
    "Mrs. Higgins": "Mrs. Higgins gives you the real recipe. It involves 'a prayer and enough butter.'",
    "DeShawn": "DeShawn explains Milwaukee's redlining map like a TED talk. You're furious and educated.",
    "Grandma Roz": "Roz says she's seen every mayor come and go. 'They all hate potholes. None fix them.'",
    "Jen": "Jen says Harbor District money 'doesn't trickle down. It yachts past.'",
}

MILWAUKEE_LORE_SNIPPETS = [
    "Fun fact: Milwaukee was once the beer capital of the world. Your liver remembers.",
    "The 414 area code is a personality type.",
    "Cream City brick got its name from color, not dairy — but we lean into it anyway.",
    "Someone nearby is debating whether it's 'bubbler' or 'water fountain.' Do not engage.",
    "Polish Moon Tavern is a lighthouse for lost souls on the South Side.",
    "The Mitchell Park Domes are Milwaukee's glass breasts. Protect them.",
    "Deep Thought has been on the beach for months. Removal cost: $50k. Vibes: priceless.",
    "They tried to tow the Milwaukee Boat. It beached again. The city shrugged with its whole chest.",
    "The Rave pool isn't filled with water. It's filled with band graffiti and regional trauma.",
    "JJ Fish on 35th is open till 2am. The city runs on snack boxes.",
    "Ian's Mac n Cheese slice is a food group in Wisconsin.",
    "New China Buffet on 27th: endless plates, vague fortune cookies, no regrets until later.",
    "Musicians rank haunted venues nationally. The Rave wins. Milwaukee accepts this.",
    "The Grave Rave of '92 was a warehouse raid — different building, same energy.",
]

LANDMARK_FLAVOR = {
    "Sobelman's": "A temple of excess where a Bloody Mary comes with a whole fried chicken attached. The floor is sticky with the dreams of tourists.",
    "The Domes": "Three glass boobs rising from the mist. One is tropical, one is desert, and one is just for weddings. Half the glass panels are falling out, adding an element of danger to your botanical tour.",
    "The Art Museum": "The Calatrava wings open and close like a giant, expensive bird. It’s beautiful, until you realize it’s judging your outfit.",
    "The Safe House": "The worst-kept secret in the city. You have to dance like a chicken to get in, while tourists watch on a CCTV monitor and laugh at your lack of rhythm.",
    "Lake Michigan": "A vast, beautiful, and terrifyingly cold ocean. It beckons you to swim, but you know better. The alewives are watching.",
    "Milwaukee River": "It flows through downtown like a brown ribbon of history. Don't touch the water. Seriously. It smells like dead fish and regrets.",
    "Hoan Bridge": "The Hoan Bridge looms with its new anti-suicide fence. It's so effective that a local regular, 'Despair Dan', has given up on jumping because he 'can't figure out the damn geometry of the thing.' He now spends his Tuesday nights angrily eating pancakes at Ma Fischer's instead.",
    "Stop-N-Rob": "Your standard Milwaukee bodega. Owned by a dude everybody knows. The bagged tallboy is a lifestyle.",
    "Conejito's Place": "Paper plates, big portions, cheap margaritas. Silver City's living room.",
    "Ma Fischer's (Brady St)": "1212 E Brady St. Open 24 hours. Pancakes at 3am. Despair Dan is in booth four.",
    "Harbor House": "Fancy fish. Windows on the water. You can smell money and Old Bay.",
    "Coffee Makes You Black": "Amani institution. Coffee, culture, and conversations that run long.",
    "Washington Park": "The lagoon, the bandshell, and geese that own the sidewalk.",
    "El Trucko": "Mitchell Street's rolling kitchen. Hype fluctuates. Flavor does not.",
    "Art Bar": "Brady Street. Someone is in a costume. It's Tuesday. That's fine.",
    "Glory Days": "Karaoke so sincere it hurts. A guy is crying to Bon Jovi. Valid.",
    "Gee's Clippers": "Bronzeville. Haircuts and history in the same chair.",
    "Sherman Phoenix": "Black-owned businesses in a phoenix. You buy something you didn't need. Worth it.",
    "Basilica of St. Josaphat": "The dome makes you feel small in a good way. Chloe may be in the basement.",
    "Polish Center of Wisconsin": "Kielbasa, polka, and memories of a Milwaukee that still exists.",
    "America's Black Holocaust Museum": "Quiet. Heavy. Important. You leave different.",
    "Milwaukee Public Market": "Third Ward. $14 olives. Samples save you.",
    "Falcon Bowl": "Riverwest bowling. Cheap beer. Someone's band is playing too loud. Perfect.",
    "Economic Support Window": "The Center. Take a number. Regret everything.",
    "West Allis Cheese Shoppe": "Curds squeak. Packers talk mandatory.",
    "Central Library": "Beautiful, haunted by students, and home to Kennedy rituals.",
    "Deer District": "Fiserv Forum adjacent. Pretzels, playoffs energy, and strangers high-fiving you.",
    "The Rave": (
        "2401 W. Wisconsin Ave. Born 1927 as the Eagles Club and the 'Million Dollar Ballroom.' "
        "Musicians swear it's the scariest club in America. The empty basement pool is the main character: "
        "bands sign the walls, All Time Low played inside it in 2024, and everyone smells chlorine when nothing's wet. "
        "Francis Wren drowned here in 1927 — or so the ghost stories say. "
        "Ghost employee Jack tells ghost hunters to 'Get out.' Rob Zombie got spooked. "
        "Mac Miller left a message on the wall that hits different now. "
        "Buddy Holly's ghost is probably here too (he didn't actually play his last show here, but Milwaukee doesn't care). "
        "Even Atlanta the TV show did an episode about this place. Sticky floors. $12 water. All ages. Legendary."
    ),
    "Deep Thought": (
        "The SS Milwaukee energy: a 33-foot boat named Deep Thought, beached between Bradford and McKinley "
        "since October. Salvage crews failed. Someone held a DJ set. Graffiti covers the hull. "
        "It is not a landmark. It is a lifestyle. The owners are in Mississippi. The city is in denial."
    ),
}

# key must match world_events.ENCOUNTER_EFFECTS for mechanical resolution
RANDOM_ENCOUNTERS = [
    {"key": "Tumbleweave", "text": "Tumbleweave: A weave blows past like a western. Majestic. Cursed."},
    {"key": "Bridge Opening", "text": "Bridge Opening: Stuck 15 minutes. You age visibly."},
    {"key": "Found Cheese Curd", "text": "Found Cheese Curd: On the ground. Still warm. Wisconsin whispers: eat it."},
    {"key": "Kia Boys", "text": "The Kia Boys: A car on the sidewalk. Your soul leaves your body briefly."},
    {"key": "Construction Season", "text": "Construction Season: Detour since 1987. Orange barrels are the state flower."},
    {"key": "Milverine", "text": "The Milverine: Shirtless. January. Power-walking. You are blessed."},
    {"key": "Festival Parking", "text": "Festival Parking: $20 on a stranger's lawn. No receipt. No regrets."},
    {"key": "Winter Parking Ban", "text": "Winter Parking Ban: Wrong side of street. Your car is in impound purgatory."},
    {"key": "Tom Barrett", "text": "A faded 'Re-Elect Tom Barrett' sticker clings to a pole like a ghost."},
    {"key": "seagull", "text": "A seagull eyes your curds. It has seen things. It wants your lunch."},
    {"key": "Ope", "text": "Someone says 'Ope' and bumps you. You apologize to each other for five minutes."},
    {"key": "yeast", "text": "You smell yeast. Brewery or lake. Either way, it's Milwaukee."},
    {"key": "Bublr", "text": "Bublr bike share: one pedal squeaks like it's judging your caseload."},
    {"key": "County Grounds", "text": "You pass the old County Grounds. Someone says the trees remember the Brewers."},
    {"key": "414 chant", "text": "A drunk guy yells 'FO-ONE-FO!' You feel hometown pride and mild anxiety."},
    {"key": "butter burger", "text": "You find a discarded Culver's wrapper. The butter aura heals you slightly."},
    {"key": "snow emergency", "text": "Snow Emergency text: move your car or become municipal art."},
    {"key": "Fiserv", "text": "Fiserv Forum glows. Bucks in six, forever, in your heart."},
    {"key": "tornado siren", "text": "Tornado siren test. Everyone ignores it except you. Stress spike."},
    {"key": "pickleball", "text": "Pickleballers have occupied every public court. War is coming."},
    {"key": "cannabis smell", "text": "That smell on the bus isn't incense. Everyone pretends. You relax slightly."},
    {"key": "DMV line", "text": "You drive past the DMV. The line is out the door. You feel secondhand stress."},
    {"key": "Polish Moon", "text": "Polish Moon's sign glows. A beacon for everyone who ever needed one more drink."},
    {
        "key": "Deep Thought",
        "text": (
            "You visit Deep Thought, the abandoned boat everyone keeps visiting. "
            "Someone tagged it 'SS MILWAUKEE.' A DJ played here last week. "
            "Salvage failed again. You take a photo. This is tourism now."
        ),
    },
    {"key": "bubbler", "text": "Someone says 'bubbler.' Someone else says 'drinking fountain.' A third person says 'we're all thirsty.'"},
    {"key": "palermos", "text": "You argue Palermo's vs. Gianelli's pizza. No one wins. Everyone's hungry."},
    {"key": "county stadium", "text": "You drive past where County Stadium was. A ghost foul pole waves in your heart."},
    {"key": "mke_airport", "text": "A plane to Phoenix takes off. A snowbird waves. You stay. You are Milwaukee."},
    {
        "key": "The Rave",
        "text": (
            "You walk past The Rave on Wisconsin Ave. A tour bus unloads. "
            "Someone says the basement pool is 'haunted as hell.' You believe them. It's Milwaukee."
        ),
    },
    {
        "key": "Grave Rave",
        "text": (
            "An old head tells you about the Grave Rave — the infamous '92 warehouse raid. "
            "Cops, lasers, Milwaukee legend. Not The Rave building, but spiritually adjacent."
        ),
    },
    {
        "key": "rave_pool",
        "text": (
            "Chlorine smell hits you on the sidewalk. No pool nearby. "
            "A musician outside The Rave says: 'Yeah, that's the basement. Welcome.'"
        ),
    },
    {"key": "culvers", "text": "You drive past a Culver's. Custard calligraphy on the sign. You are home."},
    {"key": "jj_fish", "text": "Smell of JJ Fish & Chicken on the avenue. Mild sauce in the air. Divine."},
    {"key": "ians_slice", "text": "Someone walks past with an Ian's box. Mac n Cheese slice visible. Jealousy."},
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
