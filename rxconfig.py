import reflex as rx

config = rx.Config(
    app_name="nightpalette",
    telemetry_enabled=False,
    show_built_with_reflex=False,
    default_color_mode="dark",
    plugins=[rx.plugins.SitemapPlugin()],
)
