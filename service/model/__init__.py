from peewee import *
db = SqliteDatabase('foldersorter.db')
class BaseModel(Model):
    class Meta:
        database = db

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

class RuleCondition(BaseModel):
    Id = UUIDField(primary_key=True)
    RuleId = UUIDField()
    Operator: CharField()

class Condition(BaseModel):
    Id = UUIDField(primary_key=True)
    RuleConditionId = UUIDField()
    Base: CharField()
    Operator: CharField()
    Value: CharField()
    
class ConditionValue(BaseModel):
    Id = UUIDField(primary_key=True)
    ConditionId = UUIDField()
    Value: CharField()
   
class RuleOperation(BaseModel):
    Id = UUIDField(primary_key=True)
    RuleId = UUIDField()
    Operator: CharField()

class Logs(BaseModel):
    Id = UUIDField(primary_key=True)
    text = CharField()
    timestamp = TimestampField()
