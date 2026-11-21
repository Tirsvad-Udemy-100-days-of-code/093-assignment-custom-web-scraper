# Langkah 5: CSV kesihatan

🌐 [English](Step-5-Wellness-CSV) · [Dansk](Step-5-Wellness-CSV-da) · **Bahasa Melayu**

Pencapaian `MIL-005`. Cabang dan pull request: satu untuk langkah ini.

![Satu larian pengikis yang menulis CSV](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/05-wellness-csv-run.png)

## Apa yang dilakukan

Peraturan yang menanda makanan sebagai tinggi protein, tinggi serat atau rendah kalori (dan membuangnya apabila natrium tinggi), kes guna `scrape_foods` dari halaman kedudukan ke halaman makanan ke makanan yang dikekalkan, penulis `save_to_csv` dan baris perintah `python -m nutrition_scraper`. Larian langsung terhadap laman menulis CSV di komputer tempatan; CSV itu sendiri tidak di-commit.

## Apa yang diperoleh

- Modul `csv` mengurus koma dan tanda petik untuk anda; satu `DictWriter` dan senarai lajur tetap menjadikan fail boleh diramal.
- Memisahkan peraturan (domain) daripada pengambilan (infrastruktur) bermakna nilai ambang diuji dengan nombor biasa, tanpa HTML.
- Larian sebenar menunjukkan apa yang tidak dapat ditunjukkan fixture: sesetengah halaman tiada nilai bagi sesuatu nutrien, jadi setiap nilai pilihan disimpan sebagai kosong dan bukan sifar.
