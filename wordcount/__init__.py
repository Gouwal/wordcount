import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from worker import conn

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

q = Queue(connection=conn)

from . import views
