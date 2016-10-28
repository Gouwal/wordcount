from . import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.types import Text

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self,url,result_all,result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)
