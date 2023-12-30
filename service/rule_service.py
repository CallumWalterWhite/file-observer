import json
from typing import List, Optional
from service.model import Rule, RuleMonitor, RuleOperation, db
import uuid
from service.file_watcher_manager import FileWatcherManager
from service.object_mapper import ObjectMapper
from service.file_watcher.condition import Condition, ConditionName, ConditionTimer
from service.file_watcher.operation import Operation, OperationMover

def public(func):
    setattr(func, 'is_public', True)
    return func

class BaseDto(object):
    def toJSON(self):
        new_data = {key: str(value) if isinstance(value, uuid.UUID) else value for key, value in self.__dict__.get('__data__', {}).items()}
        return json.dumps(new_data)

class RuleDto(BaseDto):
    id: Optional[str]
    description: str
    
class RuleMonitorDto(BaseDto):
    id: Optional[str]
    ruleid: str
    sourcepath: str
    subfolder: bool
    
class RuleOperationDto(BaseDto):
    id: Optional[str]
    ruleid: str
    action: str
    action_value: str
    
class RuleAggregateDto(BaseDto):
    id: Optional[str]
    description: str
    rulemonitors: List[RuleMonitorDto]
    ruleoperations: List[RuleOperationDto]
    
    
#TODO: update dto to match CRUD operation
#TODO: use refelection in add request handler to remap objects when passed through to method

class RuleService(object):
    def __init__(self, file_watcher_manager: FileWatcherManager):
        self.__file_watcher_manager = file_watcher_manager
        db.create_tables([Rule, RuleMonitor, RuleOperation])

    def initialize_rules_on_file_watcher_manager(self):
        rules = Rule.select()
        for rule in rules:
            monitors = RuleMonitor.select().where(RuleMonitor.RuleId == rule.Id)
            operations = RuleOperation.select().where(RuleOperation.RuleId == rule.Id)
            for monitor in monitors:
                _operations_ = []
                for operation in operations:
                    if operation.Action == 'move':
                        _operations_.append(OperationMover(operation.Action_Value))
                _conditions_ = []
                _conditions_.append(ConditionName('test'))
                self.__file_watcher_manager.upsert_observer(monitor.Id, monitor.SourcePath, monitor.Subfolder, _operations_, _conditions_, False)
        self.__file_watcher_manager.start_observers()

    @public
    def get_all_rules_aggregate(self):
        rule_aggregate_list = []
        rules = Rule.select()

        for rule in rules:
            monitors = RuleMonitor.select().where(RuleMonitor.RuleId == rule.Id)
            operations = RuleOperation.select().where(RuleOperation.RuleId == rule.Id)

            rule_monitors = [
                {
                    'id': str(monitor.Id),
                    'ruleid': str(monitor.RuleId),
                    'sourcepath': monitor.SourcePath,
                    'subfolder': monitor.Subfolder
                } for monitor in monitors
            ]

            rule_operations = [
                {
                    'id': str(op.Id),
                    'ruleid': str(op.RuleId),
                    'action': op.Action,
                    'action_value': op.ActionValue
                } for op in operations
            ]

            rule_aggregate = {
                'id': str(rule.Id),
                'description': rule.Description,
                'rulemonitors': rule_monitors,
                'ruleoperations': rule_operations
            }

            rule_aggregate_list.append(rule_aggregate)

        return rule_aggregate_list

    @public
    def create_rule(self, body):
        rule_dto: RuleDto = ObjectMapper.map(body, RuleDto)
        rule = Rule.create(Id=uuid.uuid4(), Description=rule_dto.Description)
        return rule
    
    @public
    def update_rule(self, body):
        rule_dto: RuleDto = ObjectMapper.map(body, RuleDto)
        rule = Rule.update(Description=rule_dto.description).where(Rule.Id == rule_dto.id)
        return rule
    
    @public
    def create_rule_monitor(self, body):
        rule_monitor_dto: RuleMonitorDto = ObjectMapper.map(body, RuleMonitorDto)
        rule_monitor = RuleMonitor.create(Id=uuid.uuid4(), RuleId=rule_monitor_dto.ruleid, SourcePath=rule_monitor_dto.sourcepath, Subfolder=rule_monitor_dto.subfolder)
        return rule_monitor
    
    @public
    def update_rule_monitor(self, body):
        rule_monitor_dto: RuleMonitorDto = ObjectMapper.map(body, RuleMonitorDto)
        rule_monitor = RuleMonitor.update(RuleId=rule_monitor_dto.ruleid, SourcePath=rule_monitor_dto.sourcepath, Subfolder=rule_monitor_dto.subfolder).where(RuleMonitor.Id == rule_monitor_dto.id)
        return rule_monitor
    
    @public
    def create_rule_operation(self, body):
        rule_operation_dto: RuleOperationDto = ObjectMapper.map(body, RuleOperationDto)
        rule_operation = RuleOperation.create(Id=uuid.uuid4(), RuleId=rule_operation_dto.ruleid, Action=rule_operation_dto.action, ActionValue=rule_operation_dto.action_value)
        return rule_operation
    
    @public
    def update_rule_operation(self, body):
        rule_operation_dto: RuleOperationDto = ObjectMapper.map(body, RuleOperationDto)
        rule_operation = RuleMonitor.update(RuleId=rule_operation_dto.ruleid, Action=rule_operation_dto.action, ActionValue=rule_operation_dto.action_value).where(RuleMonitor.Id == rule_operation_dto.id)
        return rule_operation
        