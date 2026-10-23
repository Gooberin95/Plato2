# Night Palette

A neighborhood coffee room on Cadmium Row in fictional Port Meridian: a hero, a menu, a drink builder that totals the order, hours and a walking map, and a Thursday open-mic chalkboard. Built with [Reflex](https://reflex.dev/) 0.10.0.

The whole site sits on one abstract mural (`assets/background.jpg`). It is painted once on the page root with `background_size="cover"`, `background_position="center"`, and `background_attachment="fixed"`, so it stays put while you scroll. Sections use dark translucent panels so the type stays readable and the painting shows through the gaps.

## Python version

Reflex 0.10.0 supports Python 3.14 (`requires-python >=3.11,<4`, with a Python 3.14 classifier). This project targets **Python 3.14.4**.

## Run it on Ubuntu

From a terminal:

```bash
git clone https://github.com/Gooberin95/Plato2.git
cd Plato2
```

Install Python 3.14.4 and expose it as `python3.14` (skip this block if `python3.14 --version` already prints `Python 3.14.4`):

```bash
sudo apt update
sudo apt install -y curl ca-certificates
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv python install 3.14.4
mkdir -p "$HOME/.local/bin"
ln -sfn "$(uv python find 3.14.4)" "$HOME/.local/bin/python3.14"
export PATH="$HOME/.local/bin:$PATH"
python3.14 --version
```

Create a virtual environment, install Reflex, and start the app. The repo is already a Reflex project (`rxconfig.py`, the `nightpalette` package, and `assets/` are included), so do **not** run `reflex init` — it will offer to overwrite these files.

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
reflex run
```

The first `reflex run` compiles the frontend and downloads Reflex's frontend toolchain, so it needs a network connection and a minute or two. When it is ready, open:

**http://localhost:3000**

The backend listens on http://localhost:8000. You do not need to open that URL. Stop the app with Ctrl+C.

## Deploying to Azure

Production deploys go to Azure App Service on Linux, using the built-in Python 3.14 runtime and no Docker. The GitHub Actions workflow builds the Reflex frontend, packages it with the Python app, and lets App Service install dependencies and start `startup.sh`. The staging and production jobs stay skipped until the repository variable `AZURE_DEPLOY_ENABLED` is `true`. The full setup is in [DEPLOY.md](DEPLOY.md).

## Pages

- `/` — the room, today's bar, and a few drinks worth building
- `/menu` — drinks, pastries, and the seasonal card
- `/slip` — build a drink and see the total
- `/evenings` — the calendar and the open-mic chalkboard
- `/visit` — hours and the walk from Lantern Wharf
