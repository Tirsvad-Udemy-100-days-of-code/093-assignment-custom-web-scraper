# Installation

🌐 [English](Install) · **Dansk** · [Bahasa Melayu](Install-ms)

Opret et lokalt virtuelt miljø i `.venv`, opgrader pip og installer projektet med dets testværktøjer. Du skal bruge Python 3.14 eller nyere.

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

Kør skraberen (den venter 2 s mellem forespørgsler og skriver `data/wellness_foods.csv`):

```bash
python -m nutrition_scraper
```

Kør testene:

```bash
python -m pytest
```
