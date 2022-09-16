from datetime import datetime
#from utils.db import db
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Departments(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    departments = db.Column(db.String(100))
    deptF = db.relationship('Hired_employees')
    

class Log_action(db.Model):
    __tablename__ = 'log_action'
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    user = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(200), nullable=False) 
    end_point = db.Column(db.String(200), nullable=False) 
    date_action = db.Column(db.DateTime, nullable=False)

class Hired_employees(db.Model):
    __tablename__ = 'hired_employees'
    id = db.Column(db.Integer, primary_key=True)    
    id_hired = db.Column(db.Integer,unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.String(200), nullable=False)
    #department_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    #job_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'),nullable=False)
    
    #@staticmethod
    #def get_count():
    #    return  Hired_employees.session.execute("SELECT * FROM hired_employees")        
    #def get_count():    
    #    return db.Query(Hired_employees).count()
        
class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(150), nullable=False)
    jobF = db.relationship('Hired_employees')
