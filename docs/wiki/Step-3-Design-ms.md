# Langkah 3: Reka bentuk

🌐 [English](Step-3-Design) · [Dansk](Step-3-Design-da) · **Bahasa Melayu**

Pencapaian `MIL-003`. Cabang dan pull request: satu untuk langkah ini.

![Kes guna UC-001](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/03-design-use-case.png)

## Apa yang dilakukan

Satu kes guna, UC-001 "Kikis makanan kesihatan ke CSV", dengan aliran alternatif (halaman yang dilarang laman, halaman tanpa nilai, permintaan yang gagal). Dua ADR merekodkan klien pustaka standard dan nilai ambang. Model domain, rajah jujukan sistem, kontrak operasi, rajah jujukan dan rajah kelas reka bentuk menunjukkan bagaimana lapisan berpadu.

## Apa yang diperoleh

- Aliran alternatif menemui kes sukar sebelum kod: apa yang dibuat apabila `robots.txt` menolak, atau halaman tiada jadual nutrien.
- Satu port (`FoodSource`) antara kes guna dan klien web membolehkan kes guna diuji dengan sumber palsu dan tanpa rangkaian.
- Menulis nilai ambang sebagai keputusan (ADR) menjelaskan bahawa "mesra kesihatan" ialah peraturan kajian yang ringkas, bukan nasihat pemakanan.
