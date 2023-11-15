"""
    DATABASE MODELS.
"""
from peewee import *
import uuid
import datetime
database = SqliteDatabase('database.sqlite3')

def to_isoformat(date) -> str:
    if isinstance(date, str):
        return date
    else:
        return date.isoformat()

class BaseModel(Model):
    class Meta:
        database = database

class Tool(BaseModel):
    SN = IntegerField(primary_key=True)
    category = CharField(max_length=255, null=False)
    platform = IntegerField()
    license_type = IntegerField()
    api_support = IntegerField()
    name = CharField(max_length=255, null=False)
    uid = CharField(max_length=255, null=False)
    description = TextField(null = False, default='')
    version = CharField(max_length=255, null=False)
    release_date = DateField(null=False)
    lastupdated_date = DateField(null=False)
    producer = CharField(max_length=255, null=False)
    rating = IntegerField()
    downloadlink = TextField(null=False, default='')
    editor_choice = IntegerField()
    
    @staticmethod
    def _to_dict(tool_object):
        if tool_object is not None:
            return {
                'SN': tool_object.SN,
                'category': tool_object.category,
                'platform': tool_object.platform,
                'license_type': tool_object.license_type,
                'api_support' : tool_object.api_support,
                'name' : tool_object.name,
                'uid' : tool_object.uid,
                'description' : tool_object.description,
                'version' : tool_object.version,
                'release_date' : to_isoformat(tool_object.release_date),
                'lastupdated_date' : to_isoformat(tool_object.lastupdated_date),
                'producer' : tool_object.producer,
                'rating' : tool_object.rating,
                'downloadlink' : tool_object.downloadlink,
                'editor_choice' : tool_object.editor_choice,
            }
        return None

class Reference(BaseModel):
    SN = IntegerField(primary_key=True)
    name = CharField(max_length=255, null=False)
    type = CharField(max_length=255, null=False)
    url = TextField(null = False, default='')
    summary = TextField(null=False, default='')

    @staticmethod
    def _to_dict(reference_object):
        if reference_object is not None:
            return {
                'SN': reference_object.SN,
                'name': reference_object.name,
                'type': reference_object.type,
                'url': reference_object.url,
                'summary': reference_object.summary
            }
        return None

def create_tables():
    with database:
        database.create_tables([Tool, Reference])
