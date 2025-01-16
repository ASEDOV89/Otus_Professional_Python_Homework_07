import socket
import threading
import os

HOST = 'localhost'
PORT = 8080
DOCUMENT_ROOT = './www'

def handle_request(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        headers = request.split('\n')
        method, path, _ = headers[0].split()
        if path == '/':
            path = '/index.html'
        file_path = DOCUMENT_ROOT + path
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                response_body = file.read()
            response_headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n'
        else:
            response_body = b'404 Not Found'
            response_headers = 'HTTP/1.1 404 Not Found\r\nContent-Length: 13\r\n\r\n'
        if method == 'GET':
            client_socket.send(response_headers.encode() + response_body)
        elif method == 'HEAD':
            client_socket.send(response_headers.encode())
    except Exception as e:
        response = 'HTTP/1.1 500 Internal Server Error\r\n\r\n'
        client_socket.send(response.encode())
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'Смотрим HTTP на хосте {HOST} и порту {PORT} (http://{HOST}:{PORT}/) ...')
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_request, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Сервер отдыхает")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()