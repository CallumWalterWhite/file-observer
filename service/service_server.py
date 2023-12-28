from service.config import PORT
from service.model import TagPath, Logs, db
from service.tcp_request_handler import TCPRequestHandler
from service.rule_service import RuleService
from service.file_watcher_manager import FileWatcherManager

class ServiceServer:
    def __init__(self):
        self._port = PORT
        self._started = False
        self._setup_database()#
        self.file_watcher_manager = FileWatcherManager()
        self.rule_service = RuleService(self.file_watcher_manager)
        self._tcp_request_handler = TCPRequestHandler('', self._port)
        self._tcp_request_handler.add_request_handler_service(self.rule_service)
        
    def _setup_database(self):
        db.connect()
        db.create_tables([TagPath, Logs])

    def stop(self):
        self.file_watcher_manager.stop_observers()
        self._tcp_request_handler.stop_server()
        self._started = False

    def start(self):
        if self._started == False:
            self._started = True
            self.rule_service.initialize_rules_on_file_watcher_manager()
            self._tcp_request_handler.start_server()

if __name__ == '__main__':
    fwc = ServiceServer()
    fwc.start()