import socket
import os

# Fungsi untuk menjalankan web server single-threaded
def start_single_threaded_server(server_port):
    # Membuat socket TCP (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding socket ke semua IP host ('') dan port tertentu
    server_socket.bind(('', server_port))

    # Menentukan jumlah koneksi yang bisa ditangani dalam antrian (1 klien pada satu waktu)
    server_socket.listen(1)
    print(f"[RUNNING] Single-threaded server berjalan di port {server_port}...")

    # Loop utama server untuk terus melayani request
    while True:
        print("[WAITING] Menunggu koneksi klien...")

        # Menerima koneksi dari klien
        connection_socket, client_address = server_socket.accept()
        print(f"[CONNECTED] Klien terhubung dari {client_address}")

        try:
            # Menerima data (HTTP request) dari klien
            request = connection_socket.recv(1024).decode()
            print(f"[REQUEST] {request}")

            # Mengambil nama file dari request HTTP (GET /namafile.html HTTP/1.1)
            filename = request.split()[1].lstrip('/')

            # Jika file tidak ditemukan di direktori
            if not os.path.exists(filename):
                # Kirim response HTTP 404 Not Found
                response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
                connection_socket.sendall(response.encode())
            else:
                # Jika file ditemukan, baca isi file dalam mode biner
                with open(filename, 'rb') as f:
                    content = f.read()

                # Siapkan response HTTP 200 OK dengan header
                header = "HTTP/1.1 200 OK\r\n"
                header += f"Content-Length: {len(content)}\r\n"
                header += "Content-Type: text/html\r\n\r\n"

                # Kirim header + konten file ke klien
                connection_socket.sendall(header.encode() + content)

        except Exception as e:
            # Menampilkan pesan error jika terjadi kesalahan saat pemrosesan
            print(f"[ERROR] {e}")
        finally:
            # Tutup koneksi socket setelah melayani satu klien
            connection_socket.close()
            print("[CLOSED] Koneksi ditutup.\n")

# Program utama
if __name__ == "__main__":
    PORT = 6789  # Port yang digunakan oleh server (bisa diganti sesuai kebutuhan)
    start_single_threaded_server(PORT)
