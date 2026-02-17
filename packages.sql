-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 12 Feb 2026 pada 11.20
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `photo_service`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `packages`
--

CREATE TABLE `packages` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `packages`
--

INSERT INTO `packages` (`id`, `name`, `description`, `price`, `image`) VALUES
(14, 'Signature Plus', '• Layanan Prewedding (Signature).\r\n• 2 fotografer & 2 videografer.\r\n• Layanan 8 jam.\r\n• 1 Album 25x30, 11 Lembar dengan Suitecase Box.\r\n• 1 Kanvas Eksklusif 90x60 cm dengan Bingkai.\r\n• Latar Belakang Mini Studio.\r\n• Semua Foto Diedit.\r\n• Teaser Sinematik 60 detik.\r\n• Klip Sinematik 5 menit.\r\n• Liputan Pernikahan Sinematik 10-15 menit.\r\n• Flashdisk Usb.', 15000000.00, 'img/signature plus.jpg'),
(15, 'Signature', '• Layanan Prewedding (Platinum).\r\n• 2 fotografer & 2 videografer.\r\n• Layanan 8 jam.\r\n• 1 Album 25x30, 11 Lembar dengan Suitecase Box.\r\n• 1 Kanvas Eksklusif 90x60 cm dengan Bingkai.\r\n• Latar Belakang Mini Studio.\r\n• Semua Foto Diedit.\r\n• Teaser Sinematik 60 detik.\r\n• Klip Sinematik 5 menit.\r\n• Liputan Pernikahan Sinematik 10-15 menit.\r\n• Flashdisk Usb.', 13000000.00, 'img/signature.jpg'),
(16, 'Platinum', '• 2 fotografer & 2 videografer.\r\n• Layanan 8 jam.\r\n• Semua Foto Diedit.\r\n• 1 Album 25x30, 11 Lembar dengan Suitecase Box.\r\n• 1 Kanvas Eksklusif 90x60 cm dengan Bingkai.\r\n• Latar Belakang Mini Studio.\r\n• Teaser Sinematik 60 detik.\r\n• Klip Sinematik 5 menit\r\n• Liputan Pernikahan Sinematik 10-15 menit.\r\n• Flashdisk Usb.', 10000000.00, 'img/platinum.jpg'),
(17, 'Titanium', '· 2 fotografer & 2 videografer.\r\n· Layanan 8 jam.\r\n· Semua Foto Diedit.\r\n· 1 Album 25x30, 11 Lembar dengan Suitecase Box.\r\n· 1 Kanvas Eksklusif 90x60 cm dengan Bingkai.\r\n· Teaser Sinematik 60 detik.\r\n· Klip Sinematik 5 menit.\r\n· Flashdisk Usb.', 7500000.00, 'img/titanium.jpg'),
(18, 'Gold', '· 2 fotografer.\r\n· Layanan 6 jam.\r\n· Semua Foto Diedit.\r\n· 1 Album 25x30, 11 Lembar dengan Suitecase Box.\r\n· Flashdisk Usb.\r\n', 4000000.00, 'img/gold.jpg'),
(19, 'Akad', '· 1 fotografer & 1 videografer.\r\n· Layanan 4 jam.\r\n· Semua Foto Diedit.\r\n· 1 Album 25x30, 11 Lembar dengan Suitecase Box.\r\n· Teaser Sinematik 60 detik.\r\n· Klip Sinematik 5 menit.\r\n· Flashdisk Usb.', 6000000.00, 'img/akad.jpg'),
(20, ' Prewedding Signature', '· 1 fotografer & 1 videografer.\r\n· Semua Foto Diedit.\r\n· Prewedding Outdoor 6 jam, atau Prewedding Indoor 3 jam Gratis Studio Dharmawangsa (pilih salah satu).\r\n· 2 Kanvas Eksklusif 40x60.\r\n· Teaser Sinematik 60 detik.\r\n· Klip Sinematik 5 menit.', 3700000.00, 'img/prewed_signature.jpg'),
(21, 'Prewedding Platinum', '· 1 fotografer.\r\n· Semua Foto Diedit.\r\n· Prewedding Outdoor 6 jam, atau Prewedding Indoor 3 jam Gratis Studio Dharmawangsa (pilih salah satu).\r\n· 2 Kanvas Eksklusif 40x60.', 5700000.00, 'img/prewed_platinum.jpg'),
(22, 'Engagement, Siraman, Midodareni, Pengajian, dan lain-lain (Signature)', '· 1 fotografer & 1 videografer.\r\n· Semua Foto Diedit.\r\n· Layanan 6 jam.\r\n· Gratis 2 Cetak 45x30 dengan Bingkai Eksklusif.\r\n· Teaser Sinematik 60 detik.\r\n· Klip Sinematik 5 menit.', 4500000.00, 'img/before Signature.jpg'),
(23, 'Engagement, Siraman, Midodareni, Pengajian, dan lain-lain (Platinum)', '· 1 fotografer.\r\n· Semua Foto Diedit.\r\n· Layanan 6 jam.\r\n· Gratis 2 Cetak 45x30 dengan Bingkai Eksklusif.', 2000000.00, 'img/before Platinum.jpg');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `packages`
--
ALTER TABLE `packages`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `packages`
--
ALTER TABLE `packages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
