# Langkah 4: Pengikis

🌐 [English](Step-4-Scraper) · [Dansk](Step-4-Scraper-da) · **Bahasa Melayu**

Pencapaian `MIL-004`. Cabang dan pull request: satu untuk langkah ini.

![Ujian pengikis dengan liputan 99 %](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/04-scraper-tests.png)

## Apa yang dilakukan

Lapisan infrastruktur: klien web yang sopan yang membaca `robots.txt` dahulu, menolak laluan yang dilarang, menghantar User-Agent yang jujur, menunggu antara permintaan dan mengulang permintaan yang gagal dalam bilangan terhad; penghurai untuk halaman kedudukan dan satu untuk halaman makanan, kedua-duanya berasaskan `html.parser`; dan ujian unit dengan fixture HTML kecil serta pengangkutan palsu, supaya tiada ujian menyentuh rangkaian.

## Apa yang diperoleh

- `urllib.robotparser` menjawab "bolehkah saya ambil ini?" dalam satu panggilan, dan menyemaknya sebelum setiap permintaan ialah kesopanan yang murah.
- `html.parser` berasaskan peristiwa: penghurai menyimpan keadaan kecil (dalam baris jadual, dalam sel pertama) dan bukan mencari dalam pokok, sebab itu fixture penting.
- Menyuntik pengangkutan dan jam menjadikan jeda dan percubaan semula boleh diuji dalam milisaat.
