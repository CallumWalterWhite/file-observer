from abc import ABC, abstractmethod
from enum import Enum

class ConditionBase(Enum):
    NAME=1,
    TIMER=2

class Condition(ABC):
    def __init__(self, condition):
        self.__condition = condition
    
    @abstractmethod
    def invoke(self, event, moved):
        pass

class ConditionName(Condition):
    def __init__(self, pattern):
        super().__init__(ConditionBase.NAME)
        self.__pattern = pattern
        
    def invoke(self, event, moved):
        pass
    
    def get_patterns(self):
        return self.__pattern
    
class ConditionTimer(Condition):
    def __init__(self, age):
        super().__init__(ConditionBase.TIMER)
        self.__age = age
        
    def invoke(self, event, moved):
        pass
    
    def check_file_age(self, file):
        pass