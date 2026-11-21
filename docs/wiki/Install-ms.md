# Pemasangan

🌐 [English](Install) · [Dansk](Install-da) · **Bahasa Melayu**

Cipta persekitaran maya setempat dalam `.venv`, naik taraf pip dan pasang projek dengan alat ujiannya. Anda memerlukan Python 3.14 atau lebih baharu.

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

Jalankan pengikis (ia menunggu 2 s antara permintaan dan menulis `data/wellness_foods.csv`):

```bash
python -m nutrition_scraper
```

Jalankan ujian:

```bash
python -m pytest
```
