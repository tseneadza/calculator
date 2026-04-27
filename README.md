# Calculator

Python-powered calculator app with web and desktop interfaces.

## Modes

- Basic: arithmetic, percentages, and floating-point math
- Scientific: advanced functions, constants, and tetration support
- Programmable: placeholder for future upgrades
- Conversions: placeholder for future upgrades

## Tech

- Backend/API: FastAPI
- Desktop wrapper: pywebview
- Frontend: vanilla HTML/CSS/JS

## Setup

```bash
cd /Users/tonyseneadza/Codehome/calculator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

### Web

```bash
source .venv/bin/activate
python src/server.py
```

Open <http://localhost:8094>.

### Desktop

```bash
source .venv/bin/activate
python src/desktop.py
```
