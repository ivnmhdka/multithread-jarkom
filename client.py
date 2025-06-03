import socket
import sys

# Fungsi utama untuk menjalankan HTTP client
def http_client(server_host, server_port, filename):
    # Membuat socket TCP (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Terhubung ke server dengan IP/host dan port yang diberikan
        client_socket.connect((server_host, int(server_port)))

        # Menyusun permintaan HTTP GET
        request_line = f"GET /{filename} HTTP/1.1\r\n"
        headers = f"Host: {server_host}\r\n\r\n"
        http_request = request_line + headers

        # Mengirimkan permintaan ke server
        client_socket.sendall(http_request.encode())

        # Menerima respons dari server (dalam potongan 1024 byte)
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        # Menampilkan seluruh isi respons (header + body)
        print(response.decode(errors='ignore'))

    except Exception as e:
        # Menampilkan pesan error jika terjadi kesalahan
        print(f"[ERROR] {e}")
    finally:
        # Menutup socket setelah selesai
        client_socket.close()

# Program utama
if __name__ == "__main__":
    # Pastikan argumen yang diberikan lengkap (host, port, dan nama file)
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
        sys.exit(1)

    # Mengambil argumen dari command line
    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]

    # Menjalankan fungsi client
    http_client(server_host, server_port, filename)
