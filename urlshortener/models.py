from peewee import Model, CharField, BigAutoField
from middleware.dbconnection import db


class BaseModel(Model):
    class Meta:
        database = db


class UrlMap(BaseModel):
    id = BigAutoField(unique=True, primary_key=True)
    url = CharField(unique=True)


def setup_models():
    db.create_tables([UrlMap], safe=True)
