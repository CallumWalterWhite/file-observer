from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from service.file_watcher.condition import ConditionName

class FileObserver:
    def __init__(self, source_id, source_hash, source, ignore_directories, operations, conditions):
        self.source_id = source_id
        self.source_hash = source_hash
        self.__operations = operations
        self.__conditions = conditions
        patterns=[]
        for pattern in [condition.get_patterns() for condition in [condition for condition in self.__conditions if isinstance(condition, ConditionName)]]:
            patterns.append(pattern)
        ignore_patterns = None
        case_sensitive = False
        self.event_handler = PatternMatchingEventHandler(
            patterns, ignore_patterns, ignore_directories, case_sensitive
        )
        self.event_handler.on_created = self.on_created
        self.event_handler.on_modified = self.on_modified
        self.event_handler.on_moved = self.on_moved
        self.path = source
        self.go_recursively = True
        self.observer = Observer()

    def on_created(self, event):
        self.move_file(event)

    def on_modified(self, event):
        self.move_file(event)

    def on_moved(self, event):
        self.move_file(event, True)

    def handle_event(self, event, moved=False):
        for operation in self.__operations:
            operation.invoke(self, event, moved)

    def stop(self):
        self.observer.stop()
        self.observer.join()
        
    def start(self):
        self.observer.schedule(self.event_handler, self.path, recursive=self.go_recursively)
        self.observer.start()