from enum import IntEnum
from abc import ABC, abstractmethod
import os
import shutil

class RuleAction(IntEnum):
    RENAME=1,
    MOVE=2

class Operation(ABC):
    def __init__(self, rule):
        self.__rule = rule
    
    def get_rule(self):
        return int(self.__rule)
    
    @abstractmethod
    def invoke(self, event, moved):
        pass
    
class OperationMover(Operation):
    def __init__(self, target):
        super().__init__(RuleAction.MOVE)
        self.__target = target
        
    def invoke(self, event, moved):
        try:
            if moved:
                target = os.path.join(self.__target, os.path.basename(event.dest_path))
                shutil.move(event.dest_path, target)
            else:
                target = os.path.join(self.__target, os.path.basename(event.src_path))
                shutil.move(event.src_path, target)
        except Exception as e:
            print(e)
            pass
    
class OperationRename(Operation):
    def __init__(self, action):
        super().__init__(RuleAction.RENAME)
        self.action = action
        
    def invoke(self, event, moved):
        try:
            if moved is False:
                directory, old_filename = os.path.split(event.src_path)
                extension = old_filename.split(".")[1]
                new_path = os.path.join(directory, f'{self.action}.{extension}')
                os.rename(event.src_path, new_path)
        except Exception as e:
            print(e)
            pass
        
