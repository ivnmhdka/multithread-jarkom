import socket
import threading
import os

# Fungsi untuk menangani permintaan dari satu klien
def handle_client(connection_socket, client_address):
    try:
        # Menerima request dari klien (maksimal 1024 byte)
        request = connection_socket.recv(1024).decode()
        print(f"[REQUEST from {client_address}] {request}")

        # Parsing permintaan HTTP GET untuk mendapatkan nama file
        filename = request.split()[1].lstrip('/')
        
        # Jika file tidak ditemukan, kirimkan response 404
        if not os.path.exists(filename):
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
            connection_socket.sendall(response.encode())
        else:
            # Buka dan baca isi file yang diminta
            with open(filename, 'rb') as f:
                content = f.read()

            # Siapkan header HTTP 200 OK
            header = "HTTP/1.1 200 OK\r\n"
            header += f"Content-Length: {len(content)}\r\n"
            header += "Content-Type: text/html\r\n\r\n"

            # Kirim header + konten file ke klien
            connection_socket.sendall(header.encode() + content)

    except Exception as e:
        # Tampilkan error jika terjadi exception
        print(f"[ERROR] {e}")
    finally:
        # Tutup koneksi dengan klien
        connection_socket.close()

# Fungsi utama untuk memulai server
def start_server(server_port):
    # Buat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket ke alamat IP dan port
    server_socket.bind(('', server_port))

    # Dengarkan koneksi masuk (maks. 5 antrian)
    server_socket.listen(5)
    print(f"[LISTENING] Server running on port {server_port}...")

    while True:
        # Terima koneksi dari klien
        client_socket, addr = server_socket.accept()
        print(f"[CONNECTED] Client {addr}")

        # Buat thread baru untuk menangani koneksi klien
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

# Menjalankan server jika file ini dijalankan langsung
if __name__ == "__main__":
    PORT = 6789
    start_server(PORT)
