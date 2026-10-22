"""Menu, hours, and evening listings for Night Palette."""

DRINKS: list[dict[str, str | float | bool]] = [
    {
        "name": "House drip",
        "price": 3.25,
        "blurb": "Rotating single origin. Today: Huehuetenango, cocoa and red apple.",
        "buildable": True,
    },
    {
        "name": "Cardamom cortado",
        "price": 4.50,
        "blurb": "Short espresso, warm milk, and cracked green cardamom.",
        "buildable": True,
    },
    {
        "name": "Saffron oat latte",
        "price": 5.25,
        "blurb": "A few threads steeped in oat milk, poured over a double shot.",
        "buildable": True,
    },
    {
        "name": "Navy cold brew",
        "price": 4.75,
        "blurb": "Steeped eighteen hours. Orange peel goes in for the last.",
        "buildable": True,
    },
    {
        "name": "Matcha cloud",
        "price": 5.50,
        "blurb": "Ceremonial grade, whisked to a froth, finished with milk.",
        "buildable": True,
    },
    {
        "name": "Smoked cocoa",
        "price": 4.50,
        "blurb": "Dutch cocoa, a pinch of smoked salt, and steamed milk.",
        "buildable": True,
    },
]

PASTRIES: list[dict[str, str | float | bool]] = [
    {
        "name": "Sesame morning bun",
        "price": 4.25,
        "blurb": "Moth Oven, next door. Black sesame and brown sugar, still warm at 8.",
        "buildable": False,
    },
    {
        "name": "Brown butter financier",
        "price": 3.75,
        "blurb": "Almond, with a crisp edge. Gone by noon on most days.",
        "buildable": False,
    },
    {
        "name": "Olive oil cake",
        "price": 4.50,
        "blurb": "A slice, not a loaf. Orange zest and a good peppery oil.",
        "buildable": False,
    },
    {
        "name": "Rye kouign-amann",
        "price": 4.75,
        "blurb": "Laminated rye, salted, and it shatters when you break it.",
        "buildable": False,
    },
    {
        "name": "Dark rye cookie",
        "price": 3.25,
        "blurb": "Cocoa nib and sea salt. One is a snack. Two is lunch.",
        "buildable": False,
    },
]

SEASONAL: list[dict[str, str | float | bool]] = [
    {
        "name": "Roasted squash latte",
        "price": 5.50,
        "blurb": "October. Squash from the Harrow Lane market, brown sugar, espresso.",
        "buildable": True,
    },
    {
        "name": "Smoked maple cortado",
        "price": 5.25,
        "blurb": "October. Maple from Saturday's stall, smoked salt, equal parts milk.",
        "buildable": True,
    },
    {
        "name": "Persimmon shrub spritz",
        "price": 5.75,
        "blurb": "Persimmon shrub and soda over ice. No caffeine, plenty of color.",
        "buildable": False,
    },
    {
        "name": "Apple butter danish",
        "price": 4.75,
        "blurb": "Moth Oven, this month only. Laminated dough, apple butter, a little salt.",
        "buildable": False,
    },
]

SIZES: list[tuple[str, float]] = [
    ("Short 8 oz", 0.0),
    ("Mug 12 oz", 0.75),
    ("Bowl 16 oz", 1.50),
]

MILKS: list[tuple[str, float]] = [
    ("Whole", 0.0),
    ("Oat", 0.65),
    ("Almond", 0.65),
    ("Sesame", 0.85),
    ("Black", 0.0),
]

EXTRAS: list[tuple[str, float]] = [
    ("Extra shot", 1.25),
    ("Cardamom", 0.50),
    ("Saffron", 0.90),
    ("Honey", 0.40),
    ("Orange oil", 0.50),
]

BUILDABLE: list[dict[str, str | float | bool]] = [
    item for item in [*DRINKS, *SEASONAL] if item["buildable"]
]

DRINK_PRICES: dict[str, float] = {str(item["name"]): float(item["price"]) for item in BUILDABLE}
SIZE_PRICES: dict[str, float] = dict(SIZES)
MILK_PRICES: dict[str, float] = dict(MILKS)
EXTRA_PRICES: dict[str, float] = dict(EXTRAS)

HOURS: list[tuple[str, str]] = [
    ("Monday", "Coffee closed. Mural open 12–4."),
    ("Tuesday – Friday", "7:30am – 6:00pm"),
    ("Saturday", "8:00am – 6:00pm"),
    ("Sunday", "8:00am – 3:00pm"),
]

EVENTS: list[dict[str, str]] = [
    {
        "when": "Every Thursday · 7:30pm",
        "title": "Open Wall",
        "detail": "Poets and short readers. Five minutes, no cover, and nobody is cut off for being new. Sign the chalkboard by 7.",
        "tag": "Open mic",
    },
    {
        "when": "First Friday · 6:30pm",
        "title": "Figure Night",
        "detail": "Draw the machine, the window, or anyone who agrees to sit still. Paper is on the house. Bring a pencil if you are particular.",
        "tag": "Sketch",
    },
    {
        "when": "Sunday · 2:00pm",
        "title": "Record Hour",
        "detail": "One neighbor, one record, played through once. We lock the door when the side ends, usually by 3:15.",
        "tag": "Listening",
    },
    {
        "when": "October 30 · from open",
        "title": "Moth Oven at the counter",
        "detail": "Apple butter danish and the roasted squash latte, while they last. The bakers stay until the tray is empty.",
        "tag": "Collaboration",
    },
    {
        "when": "November 12 · 6:00pm",
        "title": "Kiln & Co. cupping",
        "detail": "Eight seats. The roasters bring the next Huehuetenango lot. Put your name on the board and tell us you want a cup.",
        "tag": "Cupping",
    },
]

FACTS: list[tuple[str, str]] = [
    ("Roaster", "Kiln & Co., two streets toward the water."),
    ("Pastry", "Moth Oven, the next door that smells like butter."),
    ("Monday", "The counter closes. The mural stays open."),
    ("Wifi", "unfinished-mural"),
]


def money(amount: float) -> str:
    """Format a dollar amount."""
    return f"${amount:.2f}"


def plus(amount: float) -> str:
    """Format an add-on, calling out the ones that are included."""
    if amount == 0:
        return "included"
    return f"+${amount:.2f}"


def cup_total(drink: str, size: str, milk: str, extras: list[str], qty: int) -> float:
    """Total for one built drink times quantity."""
    one = (
        DRINK_PRICES[drink]
        + SIZE_PRICES[size]
        + MILK_PRICES[milk]
        + sum(EXTRA_PRICES[item] for item in extras)
    )
    return round(one * qty, 2)
