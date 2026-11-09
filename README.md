1. Inisialisasi & Pengaturan Layar
pygame.init() & WIDTH, HEIGHT = 800, 800: Mengaktifkan modul Pygame dan memperluas area jendela game menjadi 800x600 piksel dengan tema dark mode (neon cyberpunk).

Bingkai/Margin (30, 70, WIDTH-60, ...): Membuat garis pembatas di dalam jendela aplikasi agar balok, bola, dan striker tidak menempel atau mepet langsung ke tepi layar.

2. Sistem Kelas Objek Utama (Class)
Striker (Papan Pemantul): Mengatur pergerakan papan ke kiri/kanan menggunakan tombol panah, serta mendinamiskan ukuran panjang papan (bisa melebar atau menyusut karena skill).

Block (Balok): Mengatur posisi balok secara rapi (tidak mepet ke tepi) dengan efek pendaran cahaya neon (glow) dan sistem sisa nyawa balok saat terkena bola.

Ball (Bola): Mengatur pantulan bola di dinding pembatas dalam, deteksi jatuh ke bawah, dan kecepatan laju bola.

PowerUp (Skill Jatuh): Mengatur kemunculan kotak skill secara acak saat balok hancur dengan peluang 15% agar permainan lebih menantang.

3. Daftar 7 Jenis Skill (Power-Up)
Setiap skill memiliki warna dan fungsi unik saat ditangkap oleh striker:

x2 (Kuning): Menggandakan jumlah bola menjadi dua kali lipat.

x3 (Pink): Menggandakan bola menjadi tiga kali lipat (Triple-Ball).

S+ (Oranye): Mempercepat laju bola.

S- (Biru): Memperlambat laju bola (Slow Motion).

W+ (Ungu): Melebarkan ukuran papan pemantul (Wide Striker).

W- (Merah): Menyiutkan ukuran papan pemantul (Shrink Striker).

+L (Hijau): Menambah nyawa permainan (Lives +1).

4. Mekanisme Game & Kondisi Berakhir
collisionChecker: Fungsi untuk mendeteksi tabrakan (antara bola dengan striker, bola dengan balok, atau striker dengan kotak skill).

gameOver(): Menghentikan permainan saat nyawa habis dan menunggu pemain menekan tombol Spasi untuk mengulang permainan dari awal.
