import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"New client connected: {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Received message: {message}")
                    self.broadcast(message, client_socket)
                else:
                    self.client_sockets.remove(client_socket)
                    client_socket.close()
                    break
            except ConnectionResetError:
                self.client_sockets.remove(client_socket)
                client_socket.close()
                break

    def broadcast(self, message, sender_socket):
        for client_socket in self.client_sockets:
            if client_socket != sender_socket:
                client_socket.send(message.encode())

if __name__ == "__main__":
    server = ChatServer('127.3.7.63', 65535)   # you cane replace ip and port regarding to your "ipconfig" results.
    server.start()
