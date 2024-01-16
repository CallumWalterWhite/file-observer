from abc import ABC, abstractmethod
from enum import Enum

class ConditionBase(Enum):
    NAME=1,
    TIMER=2,
    EXTENSION=3

class Condition(ABC):
    def __init__(self, condition):
        self.__condition = condition
    
    @abstractmethod
    def invoke(self, event, moved):
        pass

class ConditionName(Condition):
    def __init__(self, operator, pattern_type, pattern):
        super().__init__(ConditionBase.NAME)
        self.__operator = operator
        self.__pattern_type = pattern_type
        self.__pattern = pattern
        
    def invoke(self, event, moved):
        pass
    
    def get_patterns(self):
        print(self.__pattern_type)
        print(self.__pattern)
        return self.__pattern
    
class ConditionExtension(Condition):
    def __init__(self, pattern):
        super().__init__(ConditionBase.EXTENSION)
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