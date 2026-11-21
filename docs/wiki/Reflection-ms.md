# Refleksi

🌐 [English](Reflection) · [Dansk](Reflection-da) · **Bahasa Melayu**

Tugasan Hari 93: Custom Web Scraper. Wiki membawa jurnal ini dalam bahasa Inggeris, Denmark dan Melayu.

## Bagaimana saya mendekati projek

Saya memilih laman dan soalan sebelum menulis kod: nutritionvalue.org dan "makanan mana yang menyokong kesihatan dan kecergasan?". Kemudian saya membaca peraturan laman dahulu, `robots.txt` dan syarat, kerana ia menentukan apa yang boleh dilakukan pengikis. Selepas itu saya merancang enam pencapaian, masing-masing dengan cabang dan pull request sendiri, mereka bentuk kes guna, membina pengambilan dan penghuraian dengan ujian, dan barulah menambah peraturan dan CSV.

## Apa yang mudah

- Membaca `robots.txt`: `urllib.robotparser` menjawab "bolehkah saya ambil ini?" dalam satu panggilan.
- Menulis CSV: `csv.DictWriter` dengan satu senarai lajur tetap.
- Menguji peraturan: nilai ambang ialah nombor biasa, jadi ujian tidak memerlukan HTML atau rangkaian.

## Apa yang sukar

- Membaca HTML dengan `html.parser` yang hanya memberi peristiwa. Satu jadual di dalam jadual nutrien menutup keadaan saya terlalu awal, dan lemak serta lemak tepu kosong sehingga halaman sebenar menunjukkannya. Fixture tulisan tangan tidak mempunyai jadual bersarang.
- Memutuskan maksud "mesra kesihatan". Nilai ambang ialah peraturan kajian yang ringkas, bukan nasihat, dan menulisnya sebagai ADR menjadikannya jelas.
- Kekal sopan. Dengan jeda 2 s, satu larian penuh 80 halaman mengambil kira-kira 3 minit, jadi ujian terhadap laman sebenar mesti jarang dan ujian menggunakan sumber palsu.

## Apa yang akan saya ubah pada masa akan datang

- Menyimpan satu halaman sebenar sebagai fixture lebih awal, atau menulis fixture daripada struktur halaman selepas pandangan langsung pertama.
- Menambah baris kemajuan dengan masa berbaki, supaya larian sopan yang panjang tidak kelihatan tergantung.
- Menyimpan halaman dalam cache selama sehari, supaya larian kedua tidak meminta halaman yang sama daripada laman lagi.

## Pelajaran terbesar

Pengikis ialah tetamu di laman orang lain. Kod yang mengambil adalah kecil; kebanyakan kerja ialah peraturan di sekelilingnya: apa yang dibenarkan, berapa kerap, bagaimana menyatakan siapa anda dan apa yang dibuat apabila halaman tiada. Larian langsung membaca 80 halaman makanan, mengekalkan 63 makanan dan melangkau 0 halaman.
