"""Interactive state for the slip, the menu, the chalkboard, and the door."""

import datetime

import reflex as rx

from nightpalette.data import (
    DRINK_PRICES,
    EXTRA_PRICES,
    MILK_PRICES,
    SIZE_PRICES,
    cup_total,
    money,
    plus,
)

BOARD_SEED = ["Amina V.", "Jules", "the printer from no. 4"]


def describe_shop(now: datetime.datetime) -> tuple[str, str]:
    """A short open/closed line from the machine's local clock."""
    weekday = now.weekday()
    minutes = now.hour * 60 + now.minute

    def clock(total: int) -> str:
        hour, minute = divmod(total, 60)
        suffix = "am" if hour < 12 else "pm"
        hour12 = hour % 12 or 12
        if minute == 0:
            return f"{hour12}{suffix}"
        return f"{hour12}:{minute:02d}{suffix}"

    if weekday == 0:
        if 12 * 60 <= minutes < 16 * 60:
            return ("Mural open", "The coffee counter is closed. The wall is open until 4.")
        if minutes < 12 * 60:
            return ("Closed Monday", "Studio day. The mural opens at noon. Coffee returns Tuesday.")
        return ("Closed Monday", "The mural is dark for the night. Coffee returns Tuesday at 7:30.")

    if weekday == 6:
        opens, closes, day = 8 * 60, 15 * 60, "Sunday"
    elif weekday == 5:
        opens, closes, day = 8 * 60, 18 * 60, "Saturday"
    else:
        opens, closes, day = 7 * 60 + 30, 18 * 60, "today"

    if minutes < opens:
        return ("Opens later", f"The bar opens at {clock(opens)} {day}.")
    if minutes >= closes:
        return ("Closed for the night", "The chairs are up. Hours for the next morning are on the Visit page.")
    return ("Open now", f"Serving until {clock(closes)}.")


_OPENING_LABEL, _OPENING_DETAIL = describe_shop(datetime.datetime.now())


class ShopState(rx.State):
    """Door status, refreshed when a page loads."""

    status_label: str = _OPENING_LABEL
    status_detail: str = _OPENING_DETAIL

    @rx.event
    def refresh(self):
        """Read the shop clock again."""
        label, detail = describe_shop(datetime.datetime.now())
        self.status_label = label
        self.status_detail = detail


class UIState(rx.State):
    """The mobile index overlay."""

    menu_open: bool = False

    @rx.event
    def toggle_menu(self):
        """Open or close the index."""
        self.menu_open = not self.menu_open

    @rx.event
    def close_menu(self):
        """Close the index."""
        self.menu_open = False

    @rx.event
    def visit(self, path: str):
        """Close the index and move to another page."""
        self.menu_open = False
        return rx.redirect(path)


class MenuState(rx.State):
    """Which menu card is on the wall."""

    category: str = "Drinks"

    @rx.event
    def set_category(self, value: str):
        """Switch among drinks, pastries, and the seasonal card."""
        if value in {"Drinks", "Pastries", "Seasonal"}:
            self.category = value


class OrderState(rx.State):
    """Build-a-drink calculator. The slip is a total, not a payment."""

    drink: str = "Cardamom cortado"
    size: str = "Mug 12 oz"
    milk: str = "Oat"
    extras: list[str] = []
    guest: str = ""
    qty: int = 1

    @rx.event
    def set_drink(self, value: str):
        """Choose a base drink."""
        if value in DRINK_PRICES:
            self.drink = value

    @rx.event
    def set_size(self, value: str):
        """Choose a cup size."""
        if value in SIZE_PRICES:
            self.size = value

    @rx.event
    def set_milk(self, value: str):
        """Choose a milk, or black."""
        if value in MILK_PRICES:
            self.milk = value

    @rx.event
    def set_guest(self, value: str):
        """Name on the cup. Kept short so it fits the ticket."""
        self.guest = value[:24]

    @rx.event
    def toggle_extra(self, name: str):
        """Add or remove a priced extra."""
        if name not in EXTRA_PRICES:
            return
        if name in self.extras:
            self.extras = [item for item in self.extras if item != name]
        else:
            self.extras = [*self.extras, name]

    @rx.event
    def dec_qty(self):
        """One fewer cup, never below one."""
        self.qty = max(1, self.qty - 1)

    @rx.event
    def inc_qty(self):
        """One more cup, up to six."""
        self.qty = min(6, self.qty + 1)

    @rx.event
    def clear_slip(self):
        """Reset the slip to the house cortado."""
        self.drink = "Cardamom cortado"
        self.size = "Mug 12 oz"
        self.milk = "Oat"
        self.extras = []
        self.guest = ""
        self.qty = 1

    @rx.event
    def start_with(self, drink: str):
        """Carry a menu drink onto the slip and open it."""
        if drink in DRINK_PRICES:
            self.drink = drink
        return rx.redirect("/slip")

    @rx.var
    def drink_price(self) -> str:
        """Base price of the selected drink."""
        return money(DRINK_PRICES[self.drink])

    @rx.var
    def size_price(self) -> str:
        """Size upcharge, or included."""
        return plus(SIZE_PRICES[self.size])

    @rx.var
    def milk_price(self) -> str:
        """Milk upcharge, or included."""
        return plus(MILK_PRICES[self.milk])

    @rx.var
    def milk_line(self) -> str:
        """How the milk reads on the slip."""
        if self.milk == "Black":
            return "Black"
        return f"{self.milk} milk"

    @rx.var
    def extra_lines(self) -> list[str]:
        """One slip line per selected extra."""
        return [f"{name}    {plus(EXTRA_PRICES[name])}" for name in self.extras]

    @rx.var
    def cup_name(self) -> str:
        """Trimmed name for the cup, ignoring a trailing space while typing."""
        return " ".join(self.guest.split())

    @rx.var
    def one_cup_label(self) -> str:
        """Price of a single built cup."""
        return money(cup_total(self.drink, self.size, self.milk, self.extras, 1))

    @rx.var
    def total_label(self) -> str:
        """Quantity times one cup."""
        return money(cup_total(self.drink, self.size, self.milk, self.extras, self.qty))

    @rx.var
    def qty_line(self) -> str:
        """Quantity as it reads on the slip."""
        return f"{self.qty} cups"

    @rx.var
    def each_label(self) -> str:
        """Per-cup price when more than one is ordered."""
        return money(cup_total(self.drink, self.size, self.milk, self.extras, 1)) + " each"


class BoardState(rx.State):
    """Thursday open-mic chalkboard. It lives in this browser session."""

    names: list[str] = BOARD_SEED
    notice: str = "Five minutes. Original work, or a poem you love."

    @rx.event
    def add_name(self, form_data: dict):
        """Put a name on the board for Thursday's Open Wall."""
        cleaned = " ".join(str(form_data.get("name", "")).split())
        if not cleaned:
            self.notice = "Write a name first."
            return
        if len(cleaned) > 32:
            self.notice = "Keep it short enough for the chalkboard."
            return
        if cleaned in self.names:
            self.notice = "That name is already up."
            return
        if len(self.names) >= 16:
            self.notice = "The board is full for tonight. Come Thursday and we'll see."
            return
        self.names = [*self.names, cleaned]
        self.notice = f"{cleaned} is on for Thursday."
