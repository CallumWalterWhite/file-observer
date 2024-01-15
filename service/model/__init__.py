from uuid import UUID
from peewee import *
import json
db = SqliteDatabase('foldersorter.db')
class BaseModel(Model):
    class Meta:
        database = db
    def toJSON(self):
        new_data = {key: str(value) if isinstance(value, UUID) else value for key, value in self.__dict__.get('__data__', {}).items()}
        return json.dumps(new_data)

class TagPath(BaseModel):
    id = UUIDField(primary_key=True)
    sourcepath = CharField()
    tags = CharField()
    targetpath = CharField()
    
class Rule(BaseModel):
    Id = UUIDField(primary_key=True)
    Description = CharField()
    
class RuleMonitor(BaseModel):
    Id = UUIDField(primary_key=True)
    RuleId = UUIDField()
    SourcePath = CharField()
    Subfolder: BooleanField()

# class RuleCondition(BaseModel):
#     Id = UUIDField(primary_key=True)
#     RuleId = UUIDField()
#     AggregateOperator: CharField()

class RuleCondition(BaseModel):
    Id = UUIDField(primary_key=True)
    # RuleConditionId = UUIDField()
    RuleId = UUIDField()
    Base: CharField()
    Operator: CharField()
    Type: CharField()
    Value: CharField()
    
class ConditionValue(BaseModel):
    Id = UUIDField(primary_key=True)
    ConditionId = UUIDField()
    Value: CharField()
   
class RuleOperation(BaseModel):
    Id = UUIDField(primary_key=True)
    RuleId = UUIDField()
    Action: CharField()
    ActionValue: CharField()

class Logs(BaseModel):
    Id = UUIDField(primary_key=True)
    rule_id = UUIDField()
    text = CharField()
    timestamp = TimestampField()
