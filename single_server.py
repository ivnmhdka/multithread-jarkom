import socket
import os

def start_single_threaded_server(server_port):
    # Membuat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)  # Hanya satu koneksi pada satu waktu
    print(f"[RUNNING] Single-threaded server berjalan di port {server_port}...")

    while True:
        print("[WAITING] Menunggu koneksi klien...")
        connection_socket, client_address = server_socket.accept()
        print(f"[CONNECTED] Klien terhubung dari {client_address}")

        try:
            # Menerima request dari klien
            request = connection_socket.recv(1024).decode()
            print(f"[REQUEST] {request}")

            # Ekstrak nama file dari request HTTP
            filename = request.split()[1].lstrip('/')

            if not os.path.exists(filename):
                # Jika file tidak ditemukan, kirim 404
                response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
                connection_socket.sendall(response.encode())
            else:
                with open(filename, 'rb') as f:
                    content = f.read()

                # Buat response HTTP 200 OK
                header = "HTTP/1.1 200 OK\r\n"
                header += f"Content-Length: {len(content)}\r\n"
                header += "Content-Type: text/html\r\n\r\n"

                connection_socket.sendall(header.encode() + content)

        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            # Tutup koneksi setelah selesai
            connection_socket.close()
            print("[CLOSED] Koneksi ditutup.\n")

if __name__ == "__main__":
    PORT = 6789  # Ganti jika dibutuhkan
    start_single_threaded_server(PORT)
