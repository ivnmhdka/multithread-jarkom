import socket
import threading
import os

# Fungsi untuk menangani permintaan dari satu klien
def handle_client(connection_socket, client_address):
    try:
        request = connection_socket.recv(1024).decode()
        print(f"[REQUEST from {client_address}] {request}")

        # Parsing permintaan HTTP GET
        filename = request.split()[1].lstrip('/')
        
        # Jika file tidak ditemukan
        if not os.path.exists(filename):
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
            connection_socket.sendall(response.encode())
        else:
            with open(filename, 'rb') as f:
                content = f.read()

            # Menyiapkan response HTTP
            header = "HTTP/1.1 200 OK\r\n"
            header += f"Content-Length: {len(content)}\r\n"
            header += "Content-Type: text/html\r\n\r\n"

            connection_socket.sendall(header.encode() + content)

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        connection_socket.close()

def start_server(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    print(f"[LISTENING] Server running on port {server_port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[CONNECTED] Client {addr}")

        # Membuat thread baru untuk melayani client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    PORT = 6789 
    start_server(PORT)
