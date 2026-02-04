# Analisis dan Revisi Diagram

## 1. Analisis Batasan & Scope
Sesuai dengan proposal, sistem ini dirancang khusus untuk **Admin** sebagai pengguna tunggal (Decision Support System). Tidak ada interaksi langsung dari pelanggan.

**Poin Kunci:**
*   **Aktor**: Admin.
*   **Sifat**: Prototipe (tanpa login pelanggan).
*   **Fitur**: Input Transaksi, Proses Apriori, Output Rekomendasi.

## 2. Use Case Diagram (Revisi)

```mermaid
usecaseDiagram
    actor Admin
    
    usecase "Login" as UC_Login
    usecase "Kelola Data Transaksi\n(Input Data)" as UC_Input
    usecase "Proses Analisis Data\n(Apriori)" as UC_Process
    usecase "Input Min. Support & Confidence" as UC_Params
    usecase "Lihat Aturan Asosiasi\n(Rules)" as UC_Rules
    usecase "Cari Rekomendasi Layanan" as UC_Rec

    Admin --> UC_Login
    Admin --> UC_Input
    Admin --> UC_Process
    UC_Process ..> UC_Params : <<include>>
    Admin --> UC_Rules
    Admin --> UC_Rec
```

### Deskripsi Use Case
*   **Login**: Admin masuk ke sistem untuk keamanan.
*   **Kelola Data Transaksi**: Admin mengunggah data historis (Excel/CSV).
*   **Proses Analisis Data**: Menjalankan algoritma Apriori dengan input Support & Confidence.
*   **Lihat Aturan Asosiasi**: Melihat hasil mining (Frequent Itemset & Rules).
*   **Cari Rekomendasi**: Admin memilih layanan utama, sistem menampilkan paket pendamping.

---

## 3. Activity Diagram (Revisi)

```mermaid
activityDiagram
    start
    :Admin Login ke sistem;
    :Admin Membuka halaman Input Data Pemesanan;
    :Admin Mengunggah/Input data transaksi pemesanan;
    :Sistem Melakukan Preprocessing & Validasi Data;
    :Admin Masuk ke halaman Analisis Data;
    :Admin Input parameter (Min Support & Min Confidence);
    :Admin Klik tombol "Proses Mining";
    
    partition "Sistem (Proses Backend)" {
        :Mencari Frequent Itemset;
        :Menghitung kombinasi item (2-itemset, dst);
        :Membentuk Association Rules;
        :Menyimpan aturan ke Database;
    }
    
    :Sistem Menampilkan hasil aturan (Rules) dan Lift Ratio;
    :Admin Pindah ke menu Rekomendasi Layanan;
    :Admin Memilih satu Layanan Utama;
    :Sistem Menampilkan daftar Rekomendasi yg relevan;
    :Admin Menggunakan info untuk menawar ke pelanggan;
    stop
```

## Catatan Implementasi Web
Untuk memastikan kesesuaian dengan diagram di atas pada saat implementasi:
1.  **Halaman Upload**: Sediakan form upload file (`.csv`/`.xlsx`) daripada input manual satu per satu.
2.  **Dashboard**: Tampilkan ringkasan sederhana (Jml Transaksi, Jml Rules).
3.  **Proses Mining**: Buat progress bar atau indikator loading saat backend memproses Apriori.
4.  **Tes Rekomendasi**: Dropdown pemilihan layanan utama yang responsif menampilkan hasil rules yang berkaitan.
