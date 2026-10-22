import reflex as rx

config = rx.Config(
    app_name="nightpalette",
    telemetry_enabled=False,
    show_built_with_reflex=False,
    default_color_mode="dark",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                has_background=False,
                accent_color="amber",
                gray_color="slate",
                radius="large",
                panel_background="translucent",
            )
        ),
    ],
)
