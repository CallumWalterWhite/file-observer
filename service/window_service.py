import win32event
import win32service
import win32serviceutil
import servicemanager
from service.file_watcher_client import FileWatcherClient

class FileSorterWatcherWindowService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'FileSorterWatcherService'
    _svc_display_name_ = 'File Sorter Watcher Service'
    _svc_description_ = "File sorter watcher service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.client = FileWatcherClient()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                    servicemanager.PYS_SERVICE_STARTED,
                                    (self._svc_name_,''))
        self.client.start()