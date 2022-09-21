import pandas
#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()
from models.emp import db

def get_all(model):
    data = model.query.all()
    return data

def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()

def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    commit_changes()

def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()

def sp_quarter():
    
    query= db.session.execute('call St_quarter(2021)')
    result_all = query.fetchall()
    
    all_Q = []
    for t in result_all:
        new_Q = {
            "departments": t.departments,
            "job": t.job,
            "Q_1":t.Q_1,
            "Q_2":t.Q_2,
            "Q_3":t.Q_3,
            "Q_4":t.Q_4            
        }
        all_Q.append(new_Q)
    
    commit_changes()
    
    return result_all

def commit_changes():
    db.session.commit()
