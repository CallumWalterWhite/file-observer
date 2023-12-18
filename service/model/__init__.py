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

class Logs(BaseModel):
    text = CharField()
    timestamp = TimestampField()
