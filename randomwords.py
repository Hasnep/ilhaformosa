# TODO: Get this code reviewed.

import random

adjectives = [
    "functional",
    "witty",
    "magnificent",
    "shocking",
    "intelligent",
    "halting",
    "successful",
    "naive",
    "orange",
    "beneficial",
    "ten",
    "acceptable",
    "used",
    "ceaseless",
    "flowery",
    "dusty",
    "guiltless",
    "unused",
    "ruddy",
    "mushy",
    "probable",
    "awake",
    "craven",
    "private",
    "horrible",
    "frightening",
    "brief",
    "likeable",
    "tame",
    "inconclusive",
    "tawdry",
    "judicious",
    "terrific",
    "unique",
    "puffy",
    "able",
    "adamant",
    "lackadaisical",
    "hushed",
    "six",
    "merciful",
    "clear",
    "vague",
    "wandering",
    "hissing",
    "foamy",
    "quirky",
    "evanescent",
    "neat",
    "soft",
    "confused",
    "endurable",
    "beautiful",
    "breezy",
    "parallel",
    "arrogant",
    "bumpy",
    "ready",
    "left",
    "superb",
    "gaping",
    "afraid",
    "noisy",
    "feeble",
    "adventurous",
    "steadfast",
    "chief",
    "lamentable",
    "squealing",
    "obsequious",
    "boundless",
    "lean",
    "colossal",
    "squeamish",
    "nifty",
    "tidy",
    "serious",
    "safe",
    "wrathful",
    "steady",
    "nutty",
    "elated",
    "demonic",
    "selective",
    "purring",
    "roasted",
    "silent",
    "smooth",
    "spurious",
    "stupid",
    "nervous",
    "symptomatic",
    "legal",
    "ambitious",
    "clever",
    "hungry",
    "gleaming",
    "harsh",
    "scared",
    "automatic",
    "acidic",
    "dark",
    "tall",
    "mature",
    "fallacious",
    "tiny",
    "remarkable",
    "unkempt",
    "empty",
    "profuse",
    "thirsty",
    "gaudy",
    "sour",
    "gentle",
    "delirious",
    "accurate",
    "barbarous",
    "loud",
    "loose",
    "imminent",
    "past",
    "chilly",
    "motionless",
    "plucky",
    "modern",
    "tart",
    "plausible",
    "strange",
    "gorgeous",
    "measly",
    "courageous",
    "tacit",
    "undesirable",
    "pushy",
    "lovely",
    "nine",
    "young",
    "gullible",
    "cuddly",
    "pointless",
    "elfin",
    "ugliest",
    "bite-sized",
    "lewd",
    "brown",
    "high-pitched",
    "overt",
    "flimsy",
    "mere",
    "smelly",
    "mean",
    "damaged",
    "juicy",
    "fragile",
    "makeshift",
    "tedious",
    "idiotic",
    "immense",
    "gainful",
    "dispensable",
    "useful",
    "imported",
    "glamorous",
    "four",
    "bright",
    "lame",
    "sad",
    "equable",
    "rigid",
    "hesitant",
    "one",
    "uninterested",
    "delicious",
    "plant",
    "thin",
    "belligerent",
    "known",
    "quaint",
    "quack",
    "white",
    "faulty",
    "mighty",
    "burly",
    "alert",
    "meek",
    "puny",
    "agonizing",
    "satisfying",
    "gratis",
    "alive",
    "wistful",
    "hurried",
    "glorious",
    "tasteless",
    "miniature",
    "lively",
    "productive",
    "relieved",
    "full",
    "doubtful",
    "fabulous",
    "silly",
    "steep",
    "statuesque",
    "knowing",
    "berserk",
    "separate",
    "pathetic",
    "grouchy",
    "tiresome",
    "ad hoc",
    "scary",
    "poised",
    "pale",
    "simple",
    "last",
    "unnatural",
    "possible",
    "threatening",
    "grotesque",
    "cowardly",
    "adjoining",
    "alluring",
    "glossy",
    "abounding",
    "miscreant",
    "poor",
    "conscious",
    "high",
    "alleged",
    "available",
    "amusing",
    "gruesome",
    "disgusting",
    "jumbled",
    "exclusive",
    "hideous",
    "tremendous",
    "swift",
    "exultant",
    "warm",
    "literate",
    "well-off",
    "crooked",
    "messy",
    "smoggy",
    "giant",
    "magical",
    "polite",
    "nutritious",
    "rampant",
    "possessive",
    "weak",
    "efficacious",
    "handsome",
    "grumpy",
    "ahead",
    "premium",
    "sticky",
    "zonked",
    "uttermost",
    "second-hand",
    "valuable",
    "standing",
    "excited",
    "fantastic",
    "grandiose",
    "dizzy",
    "sneaky",
    "rare",
    "stimulating",
    "breakable",
    "deserted",
    "difficult",
    "dry",
    "coherent",
    "lowly",
    "phobic",
    "greasy",
    "different",
    "determined",
    "callous",
    "funny",
    "tough",
    "bizarre",
    "many",
    "godly",
    "perpetual",
    "substantial",
    "exotic",
    "delicate",
    "animated",
    "like",
    "bewildered",
    "glistening",
    "absurd",
    "noiseless",
    "moaning",
    "longing",
    "tearful",
    "long-term",
    "imperfect",
    "hysterical",
    "uptight",
    "obtainable",
    "parsimonious",
    "organic",
    "disillusioned",
    "joyous",
    "far-flung",
    "nonchalant",
    "ruthless",
    "neighborly",
    "repulsive",
    "obeisant",
    "windy",
    "secretive",
    "dashing",
    "mindless",
    "old-fashioned",
    "supreme",
    "black-and-white",
    "victorious",
    "cagey",
    "magenta",
    "cute",
    "panoramic",
    "seemly",
    "taboo",
    "wretched",
    "lyrical",
    "marvelous",
    "good",
    "womanly",
    "splendid",
    "dear",
    "necessary",
    "mixed",
    "violet",
    "knotty",
    "rough",
    "guttural",
    "military",
    "scarce",
    "grubby",
    "upset",
    "sudden",
    "energetic",
    "wide",
    "loutish",
    "far",
    "wiggly",
    "unsuitable",
    "curious",
    "tranquil",
    "gigantic",
    "talented",
    "majestic",
    "easy",
    "lazy",
    "slippery",
    "gabby",
    "kind",
    "sweet",
    "absorbing",
    "aberrant",
    "ossified",
    "laughable",
    "scintillating",
    "tightfisted",
    "greedy",
    "unadvised",
    "future",
    "purple",
    "itchy",
    "aquatic",
    "ill-fated",
    "pastoral",
    "impartial",
    "misty",
    "incandescent",
    "capricious",
    "sparkling",
    "bouncy",
    "better",
    "versed",
    "open",
    "mountainous",
    "verdant",
    "encouraging",
    "forgetful",
    "handy",
    "charming",
    "unhealthy",
    "oval",
    "internal",
    "elegant",
    "cruel",
    "abiding",
    "square",
    "crabby",
    "flagrant",
    "truthful",
    "infamous",
    "spicy",
    "careful",
    "hellish",
    "cloistered",
    "graceful",
    "quickest",
    "tan",
    "chunky",
    "futuristic",
    "insidious",
    "distinct",
    "frantic",
    "staking",
    "sedate",
    "overconfident",
    "ludicrous",
    "telling",
    "earsplitting",
    "resolute",
    "vacuous",
    "trite",
    "wealthy",
    "complete",
    "earthy",
    "abnormal",
    "rambunctious",
    "typical",
    "dreary",
    "lucky",
    "impolite",
    "quizzical",
    "damaging",
    "first",
    "weary",
    "worthless",
    "worried",
    "tight",
    "sophisticated",
    "chemical",
    "hollow",
    "stereotyped",
    "filthy",
    "aspiring",
    "faint",
    "opposite",
    "onerous",
    "previous",
    "synonymous",
    "well-made",
    "nosy",
    "friendly",
    "erect",
    "scrawny",
    "spotless",
    "reminiscent",
    "pink",
    "humdrum",
    "spiky",
    "helpful",
    "irritating",
    "erratic",
    "robust",
    "condemned",
    "voracious",
    "elderly",
    "little",
    "perfect",
    "sordid",
    "silky",
    "fast",
    "materialistic",
    "overrated",
    "plastic",
    "slow",
    "trashy",
    "thinkable",
    "waggish",
    "combative",
    "observant",
    "dead",
    "languid",
    "penitent",
    "debonair",
    "watery",
    "powerful",
    "soggy",
    "drunk",
    "sincere",
    "outgoing",
    "deeply",
    "obnoxious",
    "peaceful",
    "aggressive",
    "illegal",
    "troubled",
    "malicious",
]
nouns = [
    "kittens",
    "fear",
    "property",
    "chalk",
    "camera",
    "grape",
    "beginner",
    "paper",
    "army",
    "slip",
    "crime",
    "step",
    "lip",
    "oven",
    "letters",
    "pig",
    "observation",
    "son",
    "lamp",
    "competition",
    "ray",
    "stitch",
    "toe",
    "note",
    "rose",
    "sleep",
    "popcorn",
    "shoe",
    "tin",
    "drain",
    "fog",
    "stew",
    "face",
    "support",
    "sheet",
    "thrill",
    "sea",
    "boot",
    "group",
    "chance",
    "eyes",
    "harbor",
    "sky",
    "friend",
    "rub",
    "parcel",
    "form",
    "story",
    "breath",
    "tent",
    "men",
    "sand",
    "rule",
    "appliance",
    "point",
    "science",
    "vest",
    "texture",
    "friction",
    "sugar",
    "sign",
    "thunder",
    "flight",
    "plane",
    "verse",
    "skate",
    "lunchroom",
    "alarm",
    "driving",
    "desk",
    "aftermath",
    "behavior",
    "change",
    "fuel",
    "cook",
    "window",
    "chin",
    "bag",
    "anger",
    "mice",
    "cats",
    "thing",
    "pin",
    "pencil",
    "birthday",
    "argument",
    "rain",
    "volleyball",
    "muscle",
    "gold",
    "force",
    "blood",
    "icicle",
    "sidewalk",
    "action",
    "fact",
    "offer",
    "foot",
    "shelf",
    "insurance",
    "servant",
    "badge",
    "detail",
    "selection",
    "duck",
    "home",
    "straw",
    "quartz",
    "arithmetic",
    "plough",
    "boat",
    "word",
    "class",
    "riddle",
    "carpenter",
    "magic",
    "pet",
    "suggestion",
    "spot",
    "minister",
    "hot",
    "horses",
    "swim",
    "scarf",
    "society",
    "veil",
    "toothbrush",
    "power",
    "potato",
    "end",
    "dad",
    "honey",
    "lumber",
    "road",
    "wrist",
    "waste",
    "turn",
    "stocking",
    "whistle",
    "quince",
    "downtown",
    "room",
    "week",
    "sleet",
    "blow",
    "health",
    "apparel",
    "peace",
    "chicken",
    "plastic",
    "creator",
    "border",
    "river",
    "purpose",
    "size",
    "laugh",
    "harmony",
    "company",
    "toys",
    "zephyr",
    "cart",
    "card",
    "copper",
    "committee",
    "governor",
    "range",
    "nose",
    "loaf",
    "nest",
    "design",
    "belief",
    "zoo",
    "battle",
    "plate",
    "sort",
    "camp",
    "songs",
    "bead",
    "hill",
    "distance",
    "mask",
    "nut",
    "wrench",
    "robin",
    "queen",
    "wine",
    "cloth",
    "cat",
    "dogs",
    "whip",
    "stage",
    "sock",
    "activity",
    "seashore",
    "pail",
    "agreement",
    "kiss",
    "shock",
    "weather",
    "spoon",
    "tree",
    "stamp",
    "drawer",
    "cream",
    "humor",
    "kick",
    "brick",
    "deer",
    "measure",
    "shake",
    "front",
    "jelly",
    "jewel",
    "cobweb",
    "heat",
    "ice",
    "mom",
    "hour",
    "chess",
    "visitor",
    "writer",
    "limit",
    "history",
    "snails",
    "cows",
    "ship",
    "porter",
    "tramp",
    "oil",
    "snake",
    "neck",
    "pickle",
    "pest",
    "exchange",
    "birth",
    "babies",
    "price",
    "comparison",
    "mother",
    "guitar",
    "credit",
    "mine",
    "memory",
    "food",
    "airplane",
    "debt",
    "tiger",
    "authority",
    "theory",
    "earth",
    "underwear",
    "tongue",
    "cabbage",
    "cherries",
    "rate",
    "lake",
    "unit",
    "rail",
    "table",
    "cave",
    "guide",
    "iron",
    "control",
    "cable",
    "books",
    "children",
    "horn",
    "cause",
    "crate",
    "aunt",
    "pets",
    "horse",
    "relation",
    "summer",
    "planes",
    "jeans",
    "rings",
    "crown",
    "branch",
    "women",
    "act",
    "place",
    "vein",
    "amusement",
    "laborer",
    "zipper",
    "jam",
    "sponge",
    "system",
    "glove",
    "scarecrow",
    "rod",
    "pancake",
    "coal",
    "airport",
    "cast",
    "value",
    "silver",
    "rainstorm",
    "sun",
    "seat",
    "picture",
    "existence",
    "religion",
    "jump",
    "team",
    "care",
    "field",
    "crack",
    "wound",
    "railway",
    "arch",
    "basketball",
    "bottle",
    "actor",
    "spring",
    "board",
    "blade",
    "ring",
    "juice",
    "moon",
    "letter",
    "achiever",
    "decision",
    "donkey",
    "plot",
    "cracker",
    "need",
    "cannon",
    "talk",
    "flag",
    "umbrella",
    "teaching",
    "smell",
    "advice",
    "shirt",
    "curve",
    "bell",
    "experience",
    "voice",
    "division",
    "zinc",
    "taste",
    "sack",
    "partner",
    "haircut",
    "pull",
    "toad",
    "account",
    "knife",
    "glass",
    "country",
    "cakes",
    "quarter",
    "brake",
    "maid",
    "hole",
    "dock",
    "shape",
    "ball",
    "ground",
    "dog",
    "spy",
    "tooth",
    "hook",
    "increase",
    "kettle",
    "dirt",
    "bike",
    "cattle",
    "boy",
    "kitty",
    "pollution",
    "bells",
    "thread",
    "rice",
    "squirrel",
    "trip",
    "stick",
    "afterthought",
    "stone",
    "calendar",
    "flower",
    "grass",
    "payment",
    "smash",
    "snakes",
    "impulse",
    "sweater",
    "bikes",
    "sail",
    "wish",
    "event",
    "way",
    "title",
    "tail",
    "smile",
    "cherry",
    "bee",
    "hat",
    "mist",
    "reason",
    "touch",
    "butter",
    "rabbit",
    "judge",
    "play",
    "star",
    "animal",
    "attack",
    "cup",
    "birds",
    "milk",
    "position",
    "sticks",
    "request",
    "night",
    "zebra",
    "pot",
    "run",
    "apparatus",
    "destruction",
    "wool",
    "metal",
    "tub",
    "fork",
    "ear",
    "discovery",
    "skin",
    "twig",
    "sink",
    "coat",
    "spade",
    "frame",
    "flock",
    "water",
    "beef",
    "scene",
    "store",
    "drink",
    "crowd",
    "sense",
    "collar",
    "hall",
    "yoke",
    "button",
    "lettuce",
    "cap",
    "stove",
    "fang",
    "jar",
    "current",
    "bite",
    "wilderness",
    "crow",
    "crook",
    "crayon",
    "cemetery",
    "house",
    "orange",
    "toy",
    "wing",
    "string",
    "pigs",
    "square",
    "development",
    "giraffe",
    "cushion",
    "daughter",
    "degree",
    "education",
    "afternoon",
    "question",
    "fish",
    "arm",
    "flame",
    "respect",
    "egg",
    "box",
    "representative",
    "doctor",
    "punishment",
    "oatmeal",
    "territory",
    "monkey",
    "believe",
    "rake",
    "shop",
    "plant",
    "club",
    "station",
    "machine",
    "pump",
    "back",
    "protest",
    "furniture",
    "rhythm",
    "girls",
    "motion",
    "adjustment",
]


def random_ship_name() -> str:
    """A function to generate a random starting name for every ship."""
    name = "The " + random.choice(adjectives) + " " + random.choice(nouns)
    return name
