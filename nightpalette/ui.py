"""Shared chrome for Night Palette. The mural is painted once, on the page root."""

import reflex as rx

from nightpalette.state import ShopState, UIState

CREAM = "#F6EFE4"
SAFFRON = "#E7A322"
LEAF = "#8FCB78"
INK = "#1A120C"
MUTED = "rgba(246, 239, 228, 0.74)"
LINE = "rgba(246, 239, 228, 0.16)"
OVERLAY = "rgba(6, 10, 24, 0.78)"
SERIF = "'Fraunces', 'Iowan Old Style', Palatino, Georgia, serif"
SANS = "'Outfit', 'Avenir Next', 'Segoe UI', sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, monospace"

NAV_LINKS = [
    ("01", "Menu", "/menu"),
    ("02", "Slip", "/slip"),
    ("03", "Evenings", "/evenings"),
    ("04", "Visit", "/visit"),
]

INDEX_LINKS = [
    ("00", "The room", "/"),
    *NAV_LINKS,
]


def eyebrow(text: str) -> rx.Component:
    """Small saffron label above a heading."""
    return rx.text(
        text,
        font_family=MONO,
        font_size="0.74rem",
        letter_spacing="0.16em",
        text_transform="uppercase",
        color=SAFFRON,
        margin="0 0 0.55rem",
    )


def panel(*children, **props) -> rx.Component:
    """A dark glass section so the mural stays readable behind the type."""
    box_props = {
        "background": OVERLAY,
        "backdrop_filter": "blur(14px)",
        "border": f"1px solid {LINE}",
        "border_radius": "20px",
        "padding": ["1.15rem", "1.3rem", "1.45rem"],
    }
    box_props.update(props)
    return rx.box(*children, **box_props)


def paper(*children, **props) -> rx.Component:
    """Cream counter slip."""
    return rx.box(
        *children,
        background="#F4E7D2",
        color=INK,
        border_radius="16px",
        padding="1.15rem 1.15rem 1.25rem",
        box_shadow="0 18px 50px rgba(0, 0, 0, 0.28)",
        **props,
    )


def pill(label: str, href: str, filled: bool = False) -> rx.Component:
    """A round navigation button."""
    return rx.link(
        label,
        href=href,
        text_decoration="none",
        display="inline-flex",
        align_items="center",
        justify_content="center",
        min_height="2.75rem",
        padding="0.65rem 1.15rem",
        border_radius="999px",
        font_family=SANS,
        font_weight="600",
        font_size="0.95rem",
        background=SAFFRON if filled else "transparent",
        color=INK if filled else CREAM,
        border=f"1px solid {SAFFRON}",
        _hover={"background": "#F6C453" if filled else "rgba(231, 163, 34, 0.16)"},
    )


def stamp() -> rx.Component:
    """The saffron NP mark."""
    return rx.box(
        rx.text(
            "NP",
            font_family=SERIF,
            font_style="italic",
            font_size="1.05rem",
            margin="0",
            color=INK,
            line_height="1",
        ),
        width="2.6rem",
        height="2.6rem",
        border_radius="8px",
        background=SAFFRON,
        display="flex",
        align_items="center",
        justify_content="center",
        flex_shrink="0",
    )


def _active(href: str):
    return rx.State.router.url.path == href


def rail_link(number: str, label: str, href: str) -> rx.Component:
    """A numbered link in the left studio rail."""
    active = _active(href)
    return rx.link(
        rx.box(
            rx.text(
                number,
                font_family=MONO,
                font_size="0.66rem",
                letter_spacing="0.08em",
                color=SAFFRON,
                margin="0",
            ),
            rx.text(
                label,
                font_family=SANS,
                font_size="0.84rem",
                color=rx.cond(active, CREAM, MUTED),
                margin="0",
            ),
            display="flex",
            flex_direction="column",
            align_items="center",
            gap="0.1rem",
        ),
        href=href,
        text_decoration="none",
        border_left=rx.cond(active, f"2px solid {SAFFRON}", "2px solid transparent"),
        padding="0.15rem 0.2rem 0.15rem 0.4rem",
        _hover={"opacity": "1"},
    )


def rail() -> rx.Component:
    """Fixed left index. Desktop only, so the painting still frames the type."""
    return rx.desktop_only(
        rx.box(
            rx.link(
                stamp(),
                href="/",
                aria_label="Night Palette, home",
                text_decoration="none",
                border_radius="10px",
                border=rx.cond(
                    _active("/"),
                    "2px solid #F6EFE4",
                    "2px solid transparent",
                ),
            ),
            rx.box(
                *[rail_link(number, label, href) for number, label, href in NAV_LINKS],
                display="flex",
                flex_direction="column",
                align_items="center",
                gap="0.85rem",
                margin_top="0.4rem",
            ),
            rx.text(
                "NIGHT PALETTE",
                writing_mode="vertical-rl",
                font_family=SERIF,
                font_style="italic",
                font_size="0.95rem",
                letter_spacing="0.18em",
                color=CREAM,
                margin_top="auto",
            ),
            position="fixed",
            top="0",
            left="0",
            height="100vh",
            width="6.5rem",
            z_index="30",
            display="flex",
            flex_direction="column",
            align_items="center",
            padding="1.05rem 0.4rem 1.2rem",
            gap="1rem",
            background="rgba(6, 10, 24, 0.55)",
            backdrop_filter="blur(16px)",
            border_right=f"1px solid {LINE}",
        )
    )


def mobile_bar() -> rx.Component:
    """Top bar used until the left rail fits."""
    return rx.mobile_and_tablet(
        rx.box(
            rx.link(stamp(), href="/", aria_label="Night Palette, home", text_decoration="none"),
            rx.link(
                "Night Palette",
                href="/",
                font_family=SERIF,
                font_style="italic",
                font_size="1.25rem",
                text_decoration="none",
                color=CREAM,
            ),
            rx.el.button(
                rx.cond(UIState.menu_open, "Close", "Index"),
                type="button",
                on_click=UIState.toggle_menu,
                aria_label="Open the page index",
                cursor="pointer",
                background="transparent",
                color=CREAM,
                border=f"1px solid {SAFFRON}",
                border_radius="999px",
                padding="0.4rem 0.85rem",
                font_family=MONO,
                font_size="0.78rem",
                letter_spacing="0.08em",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            z_index="35",
            height="4.25rem",
            display="flex",
            align_items="center",
            justify_content="space-between",
            padding="0 1rem",
            background="rgba(6, 10, 24, 0.62)",
            backdrop_filter="blur(16px)",
            border_bottom=f"1px solid {LINE}",
        )
    )


def index_jump(number: str, label: str, href: str) -> rx.Component:
    """A large link inside the mobile index."""
    return rx.el.button(
        rx.box(
            rx.text(number, font_family=MONO, font_size="0.75rem", color=SAFFRON, margin="0"),
            rx.text(
                label,
                font_family=SERIF,
                font_style="italic",
                font_size="clamp(2rem, 8vw, 3.2rem)",
                color=CREAM,
                margin="0",
                line_height="1",
            ),
            display="flex",
            flex_direction="column",
            align_items="flex-start",
            gap="0.2rem",
        ),
        type="button",
        on_click=UIState.visit(href),
        cursor="pointer",
        background="transparent",
        border="none",
        border_bottom=f"1px solid {LINE}",
        padding="0.85rem 0",
        width="100%",
        text_align="left",
    )


def mobile_index() -> rx.Component:
    """Full-screen index, the mobile version of the studio rail."""
    return rx.cond(
        UIState.menu_open,
        rx.mobile_and_tablet(
            rx.box(
                rx.box(
                    rx.text(
                        "Index",
                        font_family=MONO,
                        letter_spacing="0.16em",
                        text_transform="uppercase",
                        color=SAFFRON,
                        margin="0",
                        font_size="0.75rem",
                    ),
                    rx.el.button(
                        "Close",
                        type="button",
                        on_click=UIState.close_menu,
                        cursor="pointer",
                        background="transparent",
                        color=CREAM,
                        border=f"1px solid {LINE}",
                        border_radius="999px",
                        padding="0.35rem 0.8rem",
                        font_family=MONO,
                        font_size="0.78rem",
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="space-between",
                    margin_bottom="0.5rem",
                ),
                *[index_jump(number, label, href) for number, label, href in INDEX_LINKS],
                position="fixed",
                inset="0",
                z_index="45",
                background="rgba(6, 10, 24, 0.9)",
                backdrop_filter="blur(18px)",
                padding="1.15rem 1.25rem 2rem",
                display="flex",
                flex_direction="column",
            )
        ),
    )


def footer() -> rx.Component:
    """Closing line, hours, and address on every page."""
    return panel(
        rx.box(
            rx.box(
                rx.text(
                    "Night Palette",
                    font_family=SERIF,
                    font_style="italic",
                    font_size="1.6rem",
                    margin="0",
                ),
                rx.text(
                    "The navy wall is still unfinished. Come add a stroke on Monday.",
                    color=MUTED,
                    margin="0.4rem 0 0",
                    line_height="1.5",
                ),
            ),
            rx.box(
                rx.text("18 Cadmium Row", margin="0", font_family=MONO, font_size="0.86rem"),
                rx.text("Port Meridian", margin="0.2rem 0 0", font_family=MONO, font_size="0.86rem"),
                rx.text(
                    "Tue–Fri 7:30–6 · Sat 8–6 · Sun 8–3",
                    margin="0.55rem 0 0",
                    color=MUTED,
                    font_size="0.9rem",
                ),
            ),
            display="flex",
            flex_direction=["column", "row"],
            justify_content="space-between",
            gap="1rem",
        ),
        margin_top="1.1rem",
    )


def shell(*children) -> rx.Component:
    """Page root. The mural is applied once here and stays fixed while the page scrolls."""
    return rx.box(
        rail(),
        mobile_bar(),
        mobile_index(),
        rx.box(
            *children,
            footer(),
            width="100%",
            max_width="1120px",
            margin_x="auto",
            padding_top=["5.1rem", "5.1rem", "5.1rem", "1.6rem"],
            padding_bottom="2.4rem",
            padding_left=["1rem", "1.15rem", "1.4rem", "8.1rem"],
            padding_right=["1rem", "1.15rem", "1.5rem", "1.6rem"],
            display="flex",
            flex_direction="column",
            gap="0.95rem",
        ),
        background_color="#070b16",
        background_image="url('/background.jpg')",
        background_size="cover",
        background_position="center",
        background_attachment="fixed",
        min_height="100vh",
        color=CREAM,
        font_family=SANS,
    )


def page_intro(kicker: str, title: str, deck: str) -> rx.Component:
    """Opening panel for an interior page."""
    return panel(
        eyebrow(kicker),
        rx.el.h1(
            title,
            font_family=SERIF,
            font_weight="500",
            font_size="clamp(2.2rem, 5vw, 3.7rem)",
            line_height="1.02",
            letter_spacing="-0.03em",
            margin="0",
            color=CREAM,
        ),
        rx.text(
            deck,
            color=MUTED,
            line_height="1.55",
            margin="0.75rem 0 0",
            max_width="40rem",
        ),
    )


def status_chip() -> rx.Component:
    """Open, closed, or mural-day, from the shop clock."""
    return rx.box(
        rx.text(
            ShopState.status_label,
            font_family=MONO,
            font_size="0.74rem",
            letter_spacing="0.14em",
            text_transform="uppercase",
            color=SAFFRON,
            margin="0",
        ),
        rx.text(ShopState.status_detail, color=MUTED, margin="0.3rem 0 0", line_height="1.45"),
    )
