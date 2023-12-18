import sys
import time
import platform
from .config import PORT
from .file_watcher import FileWatcher
import socket
import threading
from multiprocessing import Process
from .model import TagPath, Logs, db

class FileWatcherService:
    def __init__(self):
        self._port = PORT
        self._fileWatchers = []
        self._setup_database()
        self._init_watchers()

    def _setup_database(self):
        db.connect()
        db.create_tables([TagPath, Logs])

    def _init_watchers(self):
        tag_paths = TagPath.select()
        for tag_path in tag_paths:
            self.add_watcher(tag_path.sourcepath, tag_path.tags, tag_path.targetpath, tag_path.id, self._log)

    def _start_tcp_server(self):
        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_socket.bind(('', self._port))
        self._tcp_socket.listen(5)
        print(f"TCP server started at port {self._port}")
        while True:
            client_socket, addr = self._tcp_socket.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=self._handle_tcp_requests, args=(client_socket,))
            client_handler.start()
    
    def _stop_tcp_server(self):
        self._tcp_socket.close()

    def _handle_tcp_requests(self, client_socket):
        request = client_socket.recv(1024)
        print(f"Received request: {request.decode('utf-8')}")
        response = "Hello from the server!"
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

    def add_watcher(self, source, tags, target, meta_id=None, callback=None):
        self._fileWatchers.append(FileWatcher(source, tags, target, meta_id, callback))

    def stop(self):
        for fileWatcher in self._fileWatchers:
            fileWatcher.stop()
        self._stop_tcp_server()

    def start(self):
        self._start_tcp_server()

    def _log(self, log):
        Logs.create(log=log)
        print(log)

def main(debug=True):
    service = FileWatcherService()
    if debug:
        debug_service_thread = threading.Thread(target=service.start)
        debug_service_thread.start()
        return
    if platform.system() == 'Windows':
        import servicemanager
        import win32serviceutil
        import win32service
        import win32event

        class MyServiceInstaller(win32serviceutil.ServiceFramework):
            _svc_name_ = 'FileSorterWatcherService'
            _svc_display_name_ = 'File Sorter Watcher Service'

            def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

            def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)

            def SvcDoRun(self):
                servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                      servicemanager.PYS_SERVICE_STARTED,
                                      (self._svc_name_, ''))
                self.main()

            def main(self):
                service.start()

        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(MyServiceInstaller)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(MyServiceInstaller)
    elif platform.system() == 'Darwin':
        import plistlib
        import os

        plist_data = {
            'Label': 'com.filesorter.watcherservice',
            'ProgramArguments': ['/usr/bin/python3', 'main.py'],
            'RunAtLoad': True,
            'KeepAlive': True,
        }

        plist_filename = 'com.filesorter.watcherservice'
        with open(plist_filename, 'wb') as plist_file:
            plistlib.dump(plist_data, plist_file)

        os.system(f'launchctl load {plist_filename}')

    else:
        print("Unsupported platform")

if __name__ == '__main__':
    main(False)
