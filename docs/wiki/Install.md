# Install

🌐 **English** · [Dansk](Install-da) · [Bahasa Melayu](Install-ms)

Create a local virtual environment in `.venv`, upgrade pip and install the project with its test tools. You need Python 3.14 or newer.

Linux and macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Windows (PowerShell):

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the scraper (it waits 2 s between requests and writes `data/wellness_foods.csv`):

```bash
python -m nutrition_scraper
```

Run the tests:

```bash
python -m pytest
```
