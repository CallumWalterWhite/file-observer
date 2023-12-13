from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import shutil
import re
import os

class Watcher(object):
    def __init__(self, source, tags, target, meta_id=None, callback=None):
        self.target = target
        patterns = []
        for tag in tags.split(' '):
            patterns.append("*" + re.sub(re.compile(r','), '', tag) + "*")
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = False
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_created = self.on_created
        my_event_handler.on_modified = self.on_modified
        my_event_handler.on_moved = self.on_moved
        path = source
        go_recursively = True
        self.observer = Observer()
        self.observer.schedule(my_event_handler, path, recursive=go_recursively)
        self.observer.start()
        self.meta_id=meta_id
        self.callback=callback

    def on_created(self, event):
        self.logging(f"hey, {event.src_path} has been created!")
        self.move_file(event)

    def on_modified(self, event):
        self.logging(f"hey buddy, {event.src_path} has been modified")
        self.move_file(event)

    def on_moved(self, event):
        self.logging(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
        self.move_file(event, True)

    def move_file(self, event, moved=False):
        try:
            if moved:
                target_path = os.path.join(self.target, os.path.basename(event.dest_path))
                shutil.move(event.dest_path, target_path)
                self.logging(f"File moved from {event.dest_path} to {target_path}")
            else:
                target_path = os.path.join(self.target, os.path.basename(event.src_path))
                shutil.move(event.src_path, target_path)
                self.logging(f"File moved from {event.src_path} to {target_path}")
        except:
            #IGNORE
            print('Exception')

    def stop(self):
        self.observer.stop()
        self.observer.join()
    
    def logging(self, log):
        print(log)
        self.callback(log)