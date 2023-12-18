import socket

class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Establish a connection to the server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_message(self, message):
        """Send a message to the server."""
        if not self.socket:
            raise RuntimeError("Socket not connected. Call connect() first.")

        try:
            self.socket.sendall(message.encode('utf-8'))
        except Exception as e:
            raise RuntimeError(f"Error sending message: {str(e)}")

    def receive_response(self):
        """Receive and return the response from the server."""
        if not self.socket:
            raise RuntimeError("Socket not connected. Call connect() first.")

        try:
            response = self.socket.recv(1024)
            return response.decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Error receiving response: {str(e)}")

    def close_connection(self):
        """Close the connection to the server."""
        if self.socket:
            self.socket.close()
