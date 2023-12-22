import json
from app.tcp_client import TCPClient
from .ui.master_gui import MasterGUI
from .config import SERVICE_PORT, SERVICE_HOST

class FolderServiceAdapter:
    def __init__(self):
        self.client = TCPClient(SERVICE_HOST, SERVICE_PORT)

    def send_command(self, command, body):
        request = {'command': command, 'body': body}
        request_json = json.dumps(request)
        try:
            self.client.connect()
            self.client.send_message(request_json)
            response = self.client.receive_response()
            print("Received response:", response)
        finally:
            self.client.close_connection()
    
    def send_command_request(self, command):
        request = {'command': command}
        request_json = json.dumps(request)
        try:
            self.client.connect()
            self.client.send_message(request_json)
            response = self.client.receive_response()
            print("Received response:", response)
        finally:
            self.client.close_connection()
        return json.loads(response)
    
    def get_list_tag_path(self):
        return self.send_command_request('list')
    
    def get_list_logs(self):
        return self.send_command_request('logs')
    
if __name__ == "__main__":
    app = MasterGUI(FolderServiceAdapter())
    app.mainloop()