# Apriori Recommendation System

Sistem pemberi rekomendasi layanan menggunakan algoritma **Apriori** untuk menemukan hubungan antar item dalam dataset transaksi.

## Konsep Utama: Support & Confidence

Dalam algoritma Apriori, terdapat dua metrik penting yang digunakan untuk mengukur kekuatan hubungan antar item:

### 1. Support (Dukungan)
**Support** menunjukkan seberapa sering suatu kombinasi item muncul dalam seluruh dataset. 
- **Rumus**: `Support(A) = (Jumlah transaksi berisi A) / (Total semua transaksi)`
- **Contoh**: Jika Support "Sewa Gedung" adalah **0.3 (30%)**, artinya layanan tersebut muncul di 3 dari 10 transaksi yang ada.
- **Kegunaan**: Membantu kita fokus pada layanan yang populer dan mengabaikan kombinasi yang munculnya sangat jarang (noise).

### 2. Confidence (Keyakinan)
**Confidence** menunjukkan seberapa kuat hubungan antar dua item. Ini mengukur kemungkinan pembeli akan mengambil layanan B jika mereka sudah mengambil layanan A.
- **Rumus**: `Confidence(A -> B) = Support(A & B) / Support(A)`
- **Contoh**: Jika Confidence "Sewa Gedung -> Dekorasi" adalah **0.8 (80%)**, artinya dari semua orang yang menyewa gedung, 80% di antaranya juga memesan dekorasi.
- **Kegunaan**: Memberikan tingkat kepastian bahwa rekomendasi yang diberikan memang memiliki hubungan yang kuat berdasarkan pola sejarah transaksi.

---

## Cara Menjalankan Proyek

### 1. Prasyarat
- Python 3.10+
- Node.js & npm

### 2. Instalasi & Menjalankan
Cukup jalankan file batch di root folder:
```bash
./run_project.bat
```
File ini akan otomatis menginstall dependensi dan menjalankan server backend (FastAPI) serta frontend (Next.js).

### 3. Akses Aplikasi
- **Local**: [http://localhost:3000](http://localhost:3000)
- **Network**: [http://[ALAMAT-IP-ANDA]:3000](http://[ALAMAT-IP-ANDA]:3000)

## Arsitektur
- **Frontend**: Next.js (Tailwind CSS, Lucide Icons)
- **Backend**: FastAPI (Python)
- **Library AI**: `mlxtend` (Apriori Algorithm)
- **Data Processing**: `pandas`
