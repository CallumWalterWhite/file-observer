from abc import ABC, abstractmethod
import os
import shutil

from enum import Enum
class RuleAction(Enum):
    RENAME=1,
    MOVE=2

class Operation(ABC):
    def __init__(self, rule):
        self.__rule = rule
    
    @abstractmethod
    def invoke(self, event, moved):
        pass
    
class OperationMover(Operation):
    def __init__(self, target):
        super().__init__(RuleAction.MOVE)
        self.__target = target
        
    def invoke(self, event, moved):
        if moved:
            self.__target = os.path.join(self.target, os.path.basename(event.dest_path))
            shutil.move(event.dest_path, self.__target)
            self.logging(f"File moved from {event.dest_path} to {self.__target}")
        else:
            self.__target = os.path.join(self.target, os.path.basename(event.src_path))
            shutil.move(event.src_path, self.__target)
            self.logging(f"File moved from {event.src_path} to {self.__target}")