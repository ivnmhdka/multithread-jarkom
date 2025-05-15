import socket
import sys

def http_client(server_host, server_port, filename):
    # Membuat socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Terhubung ke server
        client_socket.connect((server_host, int(server_port)))

        # Menyiapkan permintaan GET
        request_line = f"GET /{filename} HTTP/1.1\r\n"
        headers = f"Host: {server_host}\r\n\r\n"
        http_request = request_line + headers

        # Mengirim permintaan ke server
        client_socket.sendall(http_request.encode())

        # Menerima dan mencetak respons dari server
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        print(response.decode(errors='ignore'))  # Menampilkan hasil

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]

    http_client(server_host, server_port, filename)
