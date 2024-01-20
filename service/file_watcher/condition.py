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
        if self.__operator == 'Starts With':
            pattern_str = f'{self.__pattern}*'
        elif self.__operator == 'Ends With':
            pattern_str = f'{self.__pattern}'
        else:
            pattern_str = f'{self.__pattern}*'
        return pattern_str
    
class ConditionExtension(Condition):
    def __init__(self, operator, pattern_type, pattern):
        super().__init__(ConditionBase.EXTENSION)
        self.__operator = operator
        self.__pattern_type = pattern_type
        self.__pattern = pattern
        
    def invoke(self, event, moved):
        pass
    
    def get_patterns(self):
        if self.__operator == 'Starts With':
            pattern_str = f'.{self.__pattern}*'
        elif self.__operator == 'Ends With':
            pattern_str = f'.*{self.__pattern}'
        else:
            pattern_str = f'.{self.__pattern}'
        return pattern_str
    
class ConditionTimer(Condition):
    def __init__(self, age):
        super().__init__(ConditionBase.TIMER)
        self.__age = age
        
    def invoke(self, event, moved):
        pass
    
    def check_file_age(self, file):
        pass