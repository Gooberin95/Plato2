"""The five rooms of Night Palette, plus a missing-page note."""

import reflex as rx

from nightpalette.data import (
    DRINKS,
    EVENTS,
    EXTRAS,
    FACTS,
    HOURS,
    MILKS,
    PASTRIES,
    SEASONAL,
    SIZES,
    money,
)
from nightpalette.state import BoardState, MenuState, OrderState
from nightpalette.ui import (
    CREAM,
    INK,
    LEAF,
    LINE,
    MONO,
    MUTED,
    SAFFRON,
    SANS,
    SERIF,
    eyebrow,
    page_intro,
    panel,
    paper,
    pill,
    shell,
    status_chip,
)


def _choice(label: str, selected, setter) -> rx.Component:
    active = selected == label
    return rx.el.button(
        label,
        type="button",
        on_click=setter(label),
        cursor="pointer",
        text_align="left",
        padding="0.68rem 0.75rem",
        border_radius="12px",
        font_family=SANS,
        font_size="0.94rem",
        color=CREAM,
        background=rx.cond(active, "rgba(231, 163, 34, 0.2)", "rgba(255,255,255,0.03)"),
        border=rx.cond(active, f"1px solid {SAFFRON}", f"1px solid {LINE}"),
        _hover={"border_color": SAFFRON},
    )


def _extra_chip(name: str, price: float) -> rx.Component:
    active = OrderState.extras.contains(name)
    return rx.el.button(
        f"{name}  {money(price) if price else 'included'}",
        type="button",
        on_click=OrderState.toggle_extra(name),
        cursor="pointer",
        padding="0.55rem 0.7rem",
        border_radius="999px",
        font_family=MONO,
        font_size="0.78rem",
        color=CREAM,
        background=rx.cond(active, "rgba(231, 163, 34, 0.22)", "rgba(255,255,255,0.03)"),
        border=rx.cond(active, f"1px solid {SAFFRON}", f"1px solid {LINE}"),
    )


def _menu_card(item: dict) -> rx.Component:
    action = (
        rx.el.button(
            "Build this →",
            type="button",
            on_click=OrderState.start_with(str(item["name"])),
            cursor="pointer",
            background="transparent",
            color=SAFFRON,
            border="none",
            padding="0.85rem 0 0",
            width="fit-content",
            font_family=MONO,
            font_size="0.8rem",
            letter_spacing="0.03em",
        )
        if item["buildable"]
        else rx.box()
    )
    return panel(
        rx.box(
            rx.el.h2(
                str(item["name"]),
                font_family=SERIF,
                font_weight="500",
                font_size="1.55rem",
                margin="0",
                color=CREAM,
                line_height="1.1",
            ),
            rx.text(
                money(float(item["price"])),
                font_family=MONO,
                color=SAFFRON,
                font_size="0.92rem",
                margin="0",
                flex_shrink="0",
            ),
            display="flex",
            justify_content="space-between",
            align_items="baseline",
            gap="0.8rem",
        ),
        rx.text(str(item["blurb"]), color=MUTED, line_height="1.5", margin="0.55rem 0 0"),
        action,
        display="flex",
        flex_direction="column",
        flex=["1 1 100%", "1 1 calc(50% - 0.45rem)"],
        min_width="0",
    )


def _card_row(items: list[dict]) -> rx.Component:
    return rx.box(
        *[_menu_card(item) for item in items],
        display="flex",
        flex_wrap="wrap",
        gap="0.9rem",
        align_items="stretch",
    )


def _category_tab(label: str, count: int) -> rx.Component:
    active = MenuState.category == label
    return rx.el.button(
        rx.box(
            rx.text(label, font_family=SERIF, font_size="1.25rem", margin="0", color=CREAM),
            rx.text(
                f"{count} on the card",
                font_family=MONO,
                font_size="0.72rem",
                color=SAFFRON,
                margin="0.15rem 0 0",
            ),
            display="flex",
            flex_direction="column",
            align_items="flex-start",
        ),
        type="button",
        on_click=MenuState.set_category(label),
        cursor="pointer",
        flex="1 1 9rem",
        text_align="left",
        padding="0.85rem 0.95rem",
        border_radius="16px",
        background=rx.cond(active, "rgba(231, 163, 34, 0.18)", "rgba(6, 10, 24, 0.62)"),
        border=rx.cond(active, f"1px solid {SAFFRON}", f"1px solid {LINE}"),
        backdrop_filter="blur(12px)",
    )


def _slip_line(left, right) -> rx.Component:
    return rx.box(
        rx.text(left, margin="0"),
        rx.text(right, margin="0"),
        display="flex",
        justify_content="space-between",
        gap="1rem",
        font_family=MONO,
        font_size="0.82rem",
        padding_y="0.28rem",
        color=INK,
    )


def _extra_line(line: str) -> rx.Component:
    return rx.text(line, font_family=MONO, font_size="0.82rem", margin="0.18rem 0", color=INK)


def _chalk_name(name: str) -> rx.Component:
    return rx.text(
        name,
        font_family=SERIF,
        font_style="italic",
        font_size="1.45rem",
        margin="0",
        color=CREAM,
        padding="0.4rem 0",
        border_bottom=f"1px dashed {LINE}",
        width="100%",
    )


def _event_row(item: dict[str, str]) -> rx.Component:
    return rx.box(
        rx.box(
            width="11px",
            height="11px",
            border_radius="999px",
            background=SAFFRON,
            position="absolute",
            left="-6px",
            top="0.35rem",
        ),
        rx.text(item["when"], font_family=MONO, font_size="0.78rem", color=SAFFRON, margin="0"),
        rx.el.h2(
            item["title"],
            font_family=SERIF,
            font_weight="500",
            font_size="1.7rem",
            margin="0.25rem 0 0",
            color=CREAM,
        ),
        rx.text(item["detail"], color=MUTED, line_height="1.55", margin="0.4rem 0 0"),
        rx.text(
            item["tag"],
            font_family=MONO,
            font_size="0.72rem",
            letter_spacing="0.12em",
            text_transform="uppercase",
            color=LEAF,
            margin="0.55rem 0 0",
        ),
        position="relative",
        border_left=f"1px solid {LINE}",
        padding_left="1.15rem",
        padding_bottom="1.35rem",
    )


def _hours_row(day: str, hours: str) -> rx.Component:
    return rx.box(
        rx.text(day, margin="0"),
        rx.text(hours, margin="0", font_family=MONO, color=SAFFRON, font_size="0.88rem"),
        display="flex",
        justify_content="space-between",
        align_items="baseline",
        gap="1rem",
        flex_wrap="wrap",
        padding_y="0.62rem",
        border_bottom=f"1px solid {LINE}",
    )


def _field_label(text: str) -> rx.Component:
    return rx.text(
        text,
        font_family=MONO,
        font_size="0.72rem",
        letter_spacing="0.14em",
        text_transform="uppercase",
        color=SAFFRON,
        margin="0 0 0.45rem",
    )


def home() -> rx.Component:
    """Hero, the room's story, and a few drinks worth building."""
    return shell(
        rx.box(
            panel(
                eyebrow("Cadmium Row · Port Meridian"),
                rx.el.h1(
                    "Slow coffee beside an unfinished mural.",
                    font_family=SERIF,
                    font_weight="500",
                    font_style="italic",
                    font_size="clamp(2.8rem, 6.4vw, 5.5rem)",
                    line_height="0.96",
                    letter_spacing="-0.035em",
                    margin="0",
                    color=CREAM,
                ),
                rx.text(
                    "A neighborhood coffee room in a former sign-painter's studio. The navy wall was never finished. Neighbors still add strokes.",
                    color=MUTED,
                    line_height="1.55",
                    margin="1rem 0 0",
                    max_width="38rem",
                    font_size="1.05rem",
                ),
                rx.box(
                    pill("Read the menu", "/menu", filled=True),
                    pill("Build a drink", "/slip"),
                    display="flex",
                    flex_direction=["column", "row"],
                    gap="0.7rem",
                    margin_top="1.25rem",
                    align_items=["stretch", "center"],
                ),
                rx.box(status_chip(), margin_top="1.2rem"),
                flex=["1 1 auto", "1 1 auto", "1.35 1 0"],
                min_width="0",
            ),
            paper(
                rx.text(
                    "Today on the bar",
                    font_family=MONO,
                    font_size="0.72rem",
                    letter_spacing="0.14em",
                    text_transform="uppercase",
                    margin="0",
                    color="rgba(26, 18, 12, 0.62)",
                ),
                rx.el.h2(
                    "Huehuetenango",
                    font_family=SERIF,
                    font_weight="500",
                    font_size="2rem",
                    margin="0.35rem 0 0",
                    line_height="1",
                ),
                rx.text(
                    "Washed. Cocoa, red apple, a clean finish. On drip until the urn is quiet.",
                    margin="0.45rem 0 0",
                    line_height="1.45",
                ),
                rx.box(height="1px", background="rgba(26, 18, 12, 0.15)", margin="0.85rem 0"),
                rx.text("From Moth Oven", font_family=MONO, font_size="0.75rem", margin="0"),
                rx.text(
                    "Sesame morning bun",
                    font_family=SERIF,
                    font_size="1.35rem",
                    margin="0.2rem 0 0",
                ),
                rx.box(height="1px", background="rgba(26, 18, 12, 0.15)", margin="0.85rem 0"),
                rx.text("Tonight", font_family=MONO, font_size="0.75rem", margin="0"),
                rx.text(
                    "Open Wall, 7:30",
                    font_family=SERIF,
                    font_style="italic",
                    font_size="1.35rem",
                    margin="0.2rem 0 0",
                ),
                rx.text("Poets. No cover. Sign the board by 7.", margin="0.25rem 0 0"),
                rx.link(
                    "See the evenings →",
                    href="/evenings",
                    color=INK,
                    font_family=MONO,
                    font_size="0.8rem",
                    margin_top="0.9rem",
                    display="inline-block",
                ),
                flex=["1 1 auto", "1 1 auto", "0.75 1 0"],
                min_width="0",
                transform=["none", "none", "rotate(-1.25deg)"],
            ),
            display="flex",
            flex_direction=["column", "column", "row"],
            gap="0.95rem",
            align_items="stretch",
        ),
        rx.box(
            *[
                panel(
                    rx.text(
                        title,
                        font_family=MONO,
                        font_size="0.72rem",
                        letter_spacing="0.14em",
                        text_transform="uppercase",
                        color=SAFFRON,
                        margin="0",
                    ),
                    rx.text(detail, margin="0.4rem 0 0", line_height="1.45"),
                    flex=["1 1 100%", "1 1 calc(50% - 0.45rem)", "1 1 calc(25% - 0.75rem)"],
                    min_width="0",
                )
                for title, detail in FACTS
            ],
            display="flex",
            flex_wrap="wrap",
            gap="0.9rem",
        ),
        panel(
            rx.box(
                rx.box(
                    eyebrow("The room"),
                    rx.el.h2(
                        "We kept the floor, the north light, and the habit of writing the specials by hand.",
                        font_family=SERIF,
                        font_weight="500",
                        font_style="italic",
                        font_size="clamp(1.7rem, 3vw, 2.35rem)",
                        line_height="1.15",
                        margin="0",
                        color=CREAM,
                    ),
                ),
                rx.box(
                    rx.text(
                        "Night Palette opened in 2014, the year the sign shop closed and left the wall half blue. Kiln & Co. roasts for us on Lantern Wharf. Moth Oven bakes before we unlock the door.",
                        color=MUTED,
                        line_height="1.6",
                        margin="0",
                    ),
                    rx.text(
                        "Monday is studio day. The room is closed for coffee and open for anyone painting the wall. Bring a brush, or just watch. Rinse brushes in the back sink.",
                        color=MUTED,
                        line_height="1.6",
                        margin="0.75rem 0 0",
                    ),
                ),
                display="flex",
                flex_direction=["column", "row"],
                gap="1.2rem",
            ),
        ),
        rx.box(
            panel(
                eyebrow("Worth building"),
                rx.el.h2(
                    "Three drinks that take a change well.",
                    font_family=SERIF,
                    font_weight="500",
                    font_size="clamp(1.8rem, 3vw, 2.4rem)",
                    margin="0",
                    color=CREAM,
                ),
                rx.text(
                    "Size, milk, and a few extras. The slip on the next page adds it up.",
                    color=MUTED,
                    margin="0.5rem 0 0",
                ),
                flex="1 1 16rem",
                min_width="0",
            ),
            *[
                _menu_card(item)
                for item in DRINKS
                if item["name"] in {"Cardamom cortado", "Saffron oat latte", "Navy cold brew"}
            ],
            display="flex",
            flex_wrap="wrap",
            gap="0.9rem",
            align_items="stretch",
        ),
    )


def menu() -> rx.Component:
    """Drinks, pastries, and the October card."""
    return shell(
        page_intro(
            "The card",
            "Drinks, pastry, and what the market did this month.",
            "Three lists. Coffee we pull all day, pastry that arrives at 7 from next door, and a short October card from Harrow Lane.",
        ),
        rx.box(
            _category_tab("Drinks", len(DRINKS)),
            _category_tab("Pastries", len(PASTRIES)),
            _category_tab("Seasonal", len(SEASONAL)),
            display="flex",
            flex_wrap="wrap",
            gap="0.7rem",
        ),
        rx.cond(
            MenuState.category == "Drinks",
            _card_row(DRINKS),
            rx.cond(
                MenuState.category == "Pastries",
                _card_row(PASTRIES),
                _card_row(SEASONAL),
            ),
        ),
    )


def slip() -> rx.Component:
    """Build a drink and watch the counter slip total it."""
    return shell(
        page_intro(
            "The slip",
            "Build a drink. We'll add it up.",
            "Pick a base, a size, a milk, and whatever belongs on top. This is a calculator for the counter. Nothing is charged here.",
        ),
        rx.box(
            panel(
                _field_label("Base"),
                rx.box(
                    *[_choice(str(item["name"]), OrderState.drink, OrderState.set_drink) for item in [*DRINKS, *SEASONAL] if item["buildable"]],
                    display="flex",
                    flex_wrap="wrap",
                    gap="0.5rem",
                ),
                rx.box(_field_label("Size"), margin_top="1.1rem"),
                rx.box(
                    *[_choice(name, OrderState.size, OrderState.set_size) for name, _price in SIZES],
                    display="flex",
                    flex_wrap="wrap",
                    gap="0.5rem",
                ),
                rx.box(_field_label("Milk"), margin_top="1.1rem"),
                rx.box(
                    *[_choice(name, OrderState.milk, OrderState.set_milk) for name, _price in MILKS],
                    display="flex",
                    flex_wrap="wrap",
                    gap="0.5rem",
                ),
                rx.text(
                    "Sesame is house-made and a little bitter. Black skips the milk entirely.",
                    color=MUTED,
                    font_size="0.88rem",
                    margin="0.45rem 0 0",
                ),
                rx.box(_field_label("Extras"), margin_top="1.1rem"),
                rx.box(
                    *[_extra_chip(name, price) for name, price in EXTRAS],
                    display="flex",
                    flex_wrap="wrap",
                    gap="0.45rem",
                ),
                rx.box(
                    rx.box(
                        _field_label("How many"),
                        rx.box(
                            rx.el.button(
                                "−",
                                type="button",
                                on_click=OrderState.dec_qty,
                                aria_label="One fewer",
                                cursor="pointer",
                                width="2.4rem",
                                height="2.4rem",
                                border_radius="999px",
                                background="transparent",
                                color=CREAM,
                                border=f"1px solid {LINE}",
                                font_size="1.2rem",
                            ),
                            rx.text(
                                OrderState.qty,
                                font_family=MONO,
                                min_width="1.4rem",
                                text_align="center",
                                margin="0",
                            ),
                            rx.el.button(
                                "+",
                                type="button",
                                on_click=OrderState.inc_qty,
                                aria_label="One more",
                                cursor="pointer",
                                width="2.4rem",
                                height="2.4rem",
                                border_radius="999px",
                                background="transparent",
                                color=CREAM,
                                border=f"1px solid {LINE}",
                                font_size="1.2rem",
                            ),
                            display="flex",
                            align_items="center",
                            gap="0.55rem",
                        ),
                    ),
                    rx.box(
                        _field_label("Name on the cup"),
                        rx.el.input(
                            value=OrderState.guest,
                            on_change=OrderState.set_guest,
                            placeholder="Optional",
                            max_length=24,
                            class_name="cup-name",
                            width="100%",
                            background="rgba(244, 231, 210, 0.92)",
                            color=INK,
                            border="1px solid rgba(26, 18, 12, 0.18)",
                            border_radius="12px",
                            padding="0.7rem 0.8rem",
                            font_family=SANS,
                        ),
                        flex="1 1 12rem",
                    ),
                    display="flex",
                    flex_wrap="wrap",
                    gap="1rem",
                    margin_top="1.15rem",
                    align_items="flex-end",
                ),
                rx.el.button(
                    "Clear the slip",
                    type="button",
                    on_click=OrderState.clear_slip,
                    cursor="pointer",
                    margin_top="1rem",
                    background="transparent",
                    color=MUTED,
                    border="none",
                    padding="0",
                    font_family=MONO,
                    font_size="0.78rem",
                    letter_spacing="0.04em",
                ),
                flex=["1 1 auto", "1 1 auto", "1.25 1 0"],
                min_width="0",
            ),
            paper(
                rx.text(
                    "Night Palette",
                    font_family=SERIF,
                    font_style="italic",
                    font_size="1.7rem",
                    margin="0",
                    line_height="1",
                ),
                rx.text(
                    "Counter slip · not a charge",
                    font_family=MONO,
                    font_size="0.72rem",
                    letter_spacing="0.08em",
                    text_transform="uppercase",
                    margin="0.35rem 0 0.7rem",
                    color="rgba(26, 18, 12, 0.6)",
                ),
                rx.box(height="1px", background="rgba(26, 18, 12, 0.16)"),
                _slip_line(OrderState.drink, OrderState.drink_price),
                _slip_line(OrderState.size, OrderState.size_price),
                _slip_line(OrderState.milk_line, OrderState.milk_price),
                rx.cond(
                    OrderState.extra_lines.length() > 0,
                    rx.foreach(OrderState.extra_lines, _extra_line),
                    rx.text(
                        "No extras",
                        font_family=MONO,
                        font_size="0.82rem",
                        margin="0.25rem 0",
                        color="rgba(26, 18, 12, 0.5)",
                    ),
                ),
                rx.box(height="1px", background="rgba(26, 18, 12, 0.16)", margin="0.45rem 0 0.35rem"),
rx.cond(
    OrderState.qty > 1,
    _slip_line(OrderState.qty_line, OrderState.each_label),
    rx.box(),
),
                rx.box(
                    rx.text("Total", font_family=MONO, font_size="0.75rem", margin="0.4rem 0 0"),
                    rx.text(
                        OrderState.total_label,
                        font_family=SERIF,
                        font_size="3.1rem",
                        line_height="0.95",
                        margin="0.15rem 0 0",
                    ),
                ),
                rx.cond(
                    OrderState.cup_name != "",
                    rx.text(
                        "For ",
                        OrderState.cup_name,
                        font_family=SERIF,
                        font_style="italic",
                        font_size="1.35rem",
                        margin="0.7rem 0 0",
                    ),
                    rx.text(
                        "No name on the cup",
                        margin="0.7rem 0 0",
                        color="rgba(26, 18, 12, 0.5)",
                        font_family=MONO,
                        font_size="0.78rem",
                    ),
                ),
                flex=["1 1 auto", "1 1 auto", "0.8 1 0"],
                min_width="0",
                align_self=["auto", "auto", "flex-start"],
                position=["static", "static", "sticky"],
                top=["auto", "auto", "1.4rem"],
            ),
            display="flex",
            flex_direction=["column", "column", "row"],
            gap="0.95rem",
            align_items="stretch",
        ),
    )


def evenings() -> rx.Component:
    """Open mic, figure night, records, and the chalkboard."""
    return shell(
        page_intro(
            "After the urn",
            "Evenings, and a chalkboard for Thursday.",
            "The room changes jobs when the laptop hour ends. Thursday is the open mic. The board below is for that night, and it lives in this browser session.",
        ),
        panel(
            eyebrow("On the calendar"),
            *[_event_row(item) for item in EVENTS],
        ),
        panel(
            eyebrow("Thursday · Open Wall"),
            rx.el.h2(
                "Put your name on the board.",
                font_family=SERIF,
                font_weight="500",
                font_size="clamp(1.8rem, 3vw, 2.5rem)",
                margin="0",
                color=CREAM,
            ),
            rx.text(BoardState.notice, color=MUTED, margin="0.45rem 0 0", line_height="1.5"),
            rx.el.form(
                rx.box(
                    rx.el.input(
                        name="name",
                        placeholder="Your name",
                        max_length=32,
                        aria_label="Name for the open mic board",
                        flex="1 1 12rem",
                        min_width="0",
                        background="rgba(255,255,255,0.04)",
                        color=CREAM,
                        border=f"1px solid {LINE}",
                        border_radius="12px",
                        padding="0.75rem 0.85rem",
                        font_family=SANS,
                    ),
                    rx.el.button(
                        "Put me on",
                        type="submit",
                        cursor="pointer",
                        background=SAFFRON,
                        color=INK,
                        border="none",
                        border_radius="999px",
                        padding="0.75rem 1.1rem",
                        font_family=SANS,
                        font_weight="600",
                    ),
                    display="flex",
                    flex_wrap="wrap",
                    gap="0.6rem",
                    margin_top="0.9rem",
                ),
                on_submit=BoardState.add_name,
                reset_on_submit=True,
            ),
rx.box(
    rx.foreach(BoardState.names, _chalk_name),
    display="flex",
    flex_direction="column",
    margin_top="1rem",
    padding_top="0.2rem",
),
            background="rgba(10, 26, 20, 0.8)",
        ),
    )


def _map() -> rx.Component:
    """A drawn corner of Cadmium Row, not a live map."""
    return rx.box(
        rx.box(
            position="absolute",
            left="7%",
            right="7%",
            top="48%",
            height="2px",
            background="rgba(246, 239, 228, 0.35)",
        ),
        rx.box(
            position="absolute",
            top="14%",
            bottom="14%",
            left="64%",
            width="2px",
            background="rgba(246, 239, 228, 0.28)",
        ),
        rx.text(
            "Cadmium Row",
            position="absolute",
            left="8%",
            top="38%",
            font_family=MONO,
            font_size="0.7rem",
            letter_spacing="0.12em",
            text_transform="uppercase",
            color=MUTED,
            margin="0",
        ),
        rx.text(
            "to the wharf",
            position="absolute",
            left="68%",
            top="16%",
            font_family=MONO,
            font_size="0.7rem",
            color=MUTED,
            margin="0",
        ),
        rx.box(
            rx.box(width="12px", height="12px", border_radius="999px", background=SAFFRON),
            rx.text("Night Palette", font_family=SERIF, font_size="1rem", margin="0.25rem 0 0"),
            position="absolute",
            left="26%",
            top="52%",
        ),
        rx.box(
            rx.box(width="10px", height="10px", border_radius="999px", background=LEAF),
            rx.text("Moth Oven", font_size="0.82rem", margin="0.2rem 0 0", color=MUTED),
            position="absolute",
            left="44%",
            top="62%",
        ),
        rx.box(
            rx.box(width="10px", height="10px", border_radius="999px", background="#4C8DFF"),
            rx.text("Lantern stair", font_size="0.82rem", margin="0.2rem 0 0", color=MUTED),
            position="absolute",
            left="68%",
            top="24%",
        ),
        position="relative",
        min_height="250px",
        border_radius="16px",
        background="rgba(5, 8, 20, 0.45)",
        border=f"1px solid {LINE}",
        overflow="hidden",
    )


def visit() -> rx.Component:
    """Hours, the walk from the wharf, and a few house rules."""
    return shell(
        page_intro(
            "Find the navy wall",
            "Hours, and how to walk here.",
            "18 Cadmium Row, Port Meridian. From Lantern Wharf, take the river stair inland and turn at the green door. We are the second room with the navy wall.",
        ),
        rx.box(
            panel(
                eyebrow("Hours"),
                status_chip(),
                rx.box(
                    *[_hours_row(day, hours) for day, hours in HOURS],
                    margin_top="0.8rem",
                ),
                flex=["1 1 auto", "1 1 auto", "1 1 0"],
                min_width="0",
            ),
            panel(
                eyebrow("The walk"),
                rx.el.h2(
                    "Second room, navy wall.",
                    font_family=SERIF,
                    font_weight="500",
                    font_size="2rem",
                    margin="0 0 0.7rem",
                    color=CREAM,
                ),
                _map(),
                rx.text(
                    "Kiln & Co. is two streets toward the water. Moth Oven is the next door.",
                    color=MUTED,
                    margin="0.75rem 0 0",
                    line_height="1.5",
                ),
                flex=["1 1 auto", "1 1 auto", "1.05 1 0"],
                min_width="0",
            ),
            display="flex",
            flex_direction=["column", "column", "row"],
            gap="0.95rem",
            align_items="stretch",
        ),
        panel(
            eyebrow("House rules"),
            rx.text("Friday after 5, laptops close. The room is for talking.", margin="0", line_height="1.5"),
            rx.text("Dogs are welcome if they can handle the grinder.", margin="0.45rem 0 0", line_height="1.5"),
            rx.text(
                "Monday brushes get rinsed in the back sink, never the espresso sink.",
                margin="0.45rem 0 0",
                line_height="1.5",
            ),
            rx.text("Wifi password: unfinished-mural.", margin="0.45rem 0 0", line_height="1.5"),
        ),
    )


def missing() -> rx.Component:
    """Shown when a path is not one of the rooms."""
    return shell(
        panel(
            eyebrow("404"),
            rx.el.h1(
                "That page isn't on the wall.",
                font_family=SERIF,
                font_weight="500",
                font_style="italic",
                font_size="clamp(2.2rem, 5vw, 3.6rem)",
                margin="0",
                color=CREAM,
            ),
            rx.text(
                "The mural continues. This address does not.",
                color=MUTED,
                margin="0.7rem 0 1rem",
            ),
            pill("Back to the room", "/", filled=True),
        ),
    )
