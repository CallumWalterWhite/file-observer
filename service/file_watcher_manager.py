from service.file_watcher.file_observer import FileObserver
from service.model import TagPath, Logs
import hashlib
import json

class FileWatcherManager(object):
    def __init__(self):
        self.__file_observers = []
        
    def upsert_observer(self, source_id, source, ignore_directories, operations, conditions, auto_start=True):
        #operations_str = json.dumps(operations, sort_keys=True)
        #conditions_str = json.dumps(conditions, sort_keys=True)
        data_to_hash = f"{source}{ignore_directories}"
        source_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        matched_observer = next((observer for observer in self.__file_observers if observer.source_id == source_id), None)
        add = True
        if matched_observer:
            if matched_observer.source_hash != source_hash:
                matched_observer.stop()
                self.__file_observers.remove(matched_observer)
            else:
                add = False
        if add:
            file_observer = FileObserver(source_id, source_hash, source, ignore_directories, operations, conditions)
            self.__file_observers.append(file_observer)
            if auto_start:
                file_observer.start()
            
    def stop_observers(self):
        for fileWatcher in self.__file_observers:
            fileWatcher.stop()
    
    def start_observers(self):
        for fileWatcher in self.__file_observers:
            fileWatcher.start()
            