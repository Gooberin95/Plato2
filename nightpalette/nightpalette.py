"""Night Palette application entrypoint."""

import reflex as rx

from nightpalette.pages import evenings, home, menu, missing, slip, visit
from nightpalette.state import ShopState

app = rx.App(
    html_lang="en",
    theme=rx.theme(
        appearance="dark",
        has_background=False,
        accent_color="amber",
        gray_color="slate",
        radius="large",
        panel_background="translucent",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;1,9..144,500;1,9..144,700&family=IBM+Plex+Mono:ital,wght@0,400;0,500;1,400&family=Outfit:wght@300;400;500;600;700&display=swap",
        "/styles.css",
    ],
    head_components=[
        rx.el.link(rel="icon", href="/favicon.svg", type="image/svg+xml"),
    ],
)

app.add_page(
    home,
    route="/",
    title="Night Palette — coffee on Cadmium Row",
    description="Slow coffee beside an unfinished mural. A neighborhood coffee room on Cadmium Row in Port Meridian.",
    image="/favicon.svg",
    on_load=ShopState.refresh,
)
app.add_page(
    menu,
    route="/menu",
    title="Menu · Night Palette",
    description="Drinks, pastries from Moth Oven, and the October card at Night Palette.",
    image="/favicon.svg",
    on_load=ShopState.refresh,
)
app.add_page(
    slip,
    route="/slip",
    title="The Slip · Night Palette",
    description="Build a drink and total it. The slip at Night Palette is a calculator, not a charge.",
    image="/favicon.svg",
    on_load=ShopState.refresh,
)
app.add_page(
    evenings,
    route="/evenings",
    title="Evenings · Night Palette",
    description="Thursday open mic, figure night, and Sunday records at Night Palette on Cadmium Row.",
    image="/favicon.svg",
    on_load=ShopState.refresh,
)
app.add_page(
    visit,
    route="/visit",
    title="Visit · Night Palette",
    description="Hours and the walk from Lantern Wharf to 18 Cadmium Row, Port Meridian.",
    image="/favicon.svg",
    on_load=ShopState.refresh,
)
app.add_page(
    missing,
    route="/404",
    title="Not on the wall · Night Palette",
    description="That page is not part of Night Palette.",
    image="/favicon.svg",
)
