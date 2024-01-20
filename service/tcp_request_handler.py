import json
import socket
import threading
import inspect
import signal

class TCPRequestHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request_handlers = {}

    def add_request_handler(self, request_type, handler_function):
        self.request_handlers[request_type] = handler_function
        
    def add_request_handler_service(self, service):
        public_methods = [method for method, _ in inspect.getmembers(service, inspect.ismethod) if getattr(_, 'is_public', False)]
        for method_name in public_methods:
            method = getattr(service, method_name)
            self.request_handlers[method_name] = method
        
    def handle_client(self, client_socket, client_address):
        request = client_socket.recv(65000)
        request_body = request.decode('utf-8')
        print(f"Received request: {request_body}")
        request_json = json.loads(request_body)
        request_command = request_json['command']
        if request_command in self.request_handlers:
            try:
                if 'body' in request_json:
                    response = self.request_handlers[request_command](request_json['body'])
                else:
                    response = self.request_handlers[request_command]()
                if hasattr(response, 'toJSON') and callable(getattr(response, 'toJSON')):
                    response_data = response.toJSON()
                else:
                    response_data = json.dumps(response)
                client_socket.send(response_data.encode('utf-8'))
            except Exception as e:
                client_socket.send(json.dumps({'status': 500,'error': str(e)}).encode('utf-8'))
        else:
            client_socket.send("Unknown request type".encode('utf-8'))
        client_socket.close()
        print(f"Connection with {client_address} closed.")

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        finally:
            self.server_socket.close()

    def stop_server(self):
        print("Server shutting down.")
        self.server_socket.close()