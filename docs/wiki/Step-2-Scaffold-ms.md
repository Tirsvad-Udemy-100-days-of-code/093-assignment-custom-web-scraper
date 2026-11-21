# Langkah 2: Rangka

🌐 [English](Step-2-Scaffold) · [Dansk](Step-2-Scaffold-da) · **Bahasa Melayu**

Pencapaian `MIL-002`. Cabang dan pull request: satu untuk langkah ini.

![Ujian asas lulus dalam .venv](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/02-scaffold-tests.png)

## Apa yang dilakukan

Projek Python kosong tetapi boleh dijalankan: `pyproject.toml` (Python 3.14 ke atas dan tiada kebergantungan runtime), pakej `src/nutrition_scraper/` dengan `constants.py`, ujian asas, `Doxyfile`, `.gitignore` Python yang turut mengabaikan data yang dikikis, `.editorconfig` dan README dengan langkah pemasangan. opengrep bersih sebelum push.

## Apa yang diperoleh

- `pyproject.toml` menyimpan metadata, senarai `dependencies` yang kosong dan tetapan pytest dalam satu fail; `pip install -e ".[dev]"` memasang alat ujian.
- Pustaka standard Python sudah cukup untuk pengikis: `urllib`, `html.parser`, `csv` dan `urllib.robotparser`.
- Meletakkan jeda, User-Agent dan nilai ambang dalam `constants.py` menjadikan kesopanan pengikis kelihatan di satu tempat dan boleh diuji sejak commit pertama.
