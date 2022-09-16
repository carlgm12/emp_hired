import redis
from flask import Flask
#from redis import Redis
from routes.service import service 
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_CONNECTION_URI
from flaskext.mysql import MySQL
from flask_migrate import Migrate
from models.emp import db

#from utils.db import db
#import MySQLdb
mysql = MySQL()

app = Flask(__name__)
redis = redis.Redis(host='redis', port=6379)
#db = MySQLdb.connect("localhost", "test", "my1234", "example")
#print(db)

# settings
app.secret_key = 'mysecret'
print(DATABASE_CONNECTION_URI)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# no cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
mysql.init_app(app)

SQLAlchemy(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(service)
