import json
from msilib.schema import ListBox
from operator import truediv
import jwt
import requests
import os
import numpy as np
import math
import time
import pandas as pd
from datetime import datetime, timedelta, timezone 
from flask import request, jsonify, session 
from doctest import OutputChecker
from urllib import response
from jwt import encode, decode, exceptions
from os import getenv
from functools import wraps 
#from example import app
from . import  database
from models.emp import Departments, Jobs, Hired_employees, Log_action
from pathlib import Path

################ funciones para descarga archivos desde el drive
################################################################
 
def download_file_from_google_drive(id, destination, file_name):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    print("confirmacion_token->",response)

    save_response_content(response, destination, file_name)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination, file_name):
    CHUNK_SIZE = 32768

    name = os.path.basename(destination) #.rsplit('.')
    dire = os.path.dirname(destination)

    full_path = f"{dire}\\{name + file_name}"

    #print("****cargando archivo****")
    
    with open(f"{dire}\\{name + file_name}", 'wb') as f:    
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        
################ funciones para el token
###########################################

def validate_token(token, output=False):
    try:
        if output:
            return decode(token,key=getenv("SECRET"), algorithms=["HS256"])
        decode(token,key=getenv("SECRET"),algorithms=["HS256"])    
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #token = request.args.get('token')    
        token = request.headers['Authorization'].split(" ")[1]
        print(request.headers['Authorization'])
    
        if not token:
            return jsonify({'message' : 'token is missing!'}), 403
        try:
            data = decode(token,key=getenv("SECRET"), algorithms=["HS256"])            
        except exceptions.DecodeError:
            response = jsonify({"message": "Invalid token"})
            response.status_code = 401
            return response
        except exceptions.ExpiredSignatureError:
            response = jsonify({"message": "Token Expired"})
            response.status_code = 401
            return response    

        return f(*args, **kwargs)
    return decorated

################ funciones De carga por lotes 
############################################

def load_job():
    print("****cargando job****")

    path_j = r'.\download\jobs.csv'

    header_list = ['id', 'job']
    df = pd.read_csv(path_j)
    df.to_csv(path_j,header=header_list,index=False)
    
    df_ = pd.read_csv(path_j)
    
    for index, row in df_.iterrows():
        print(row['job'])
        database.add_instance(Jobs, job=row['job'])

def load_departments():
    print("****cargando departments****")

    path_j = r'.\download\departments.csv'

    header_list = ['id', 'departments']
    df = pd.read_csv(path_j)
    df.to_csv(path_j,header=header_list,index=False)
    
    #enginedb = database.db.get_engine(app)
    #print(enginedb)
    df_ = pd.read_csv(path_j)
            
    for index, row in df_.iterrows():
        print(row['departments'])
        database.add_instance(Departments, departments=row['departments'])

def validate_load_hired(parm):

    path_j = r'.\download\hired_employees.csv'
    
    df_ = pd.read_csv(path_j,sep=',', names = ["id_hired", "name", "date_time", "dept_id_", "job_id"])

    # obtener maximo del archivo qui
    max_hired = df_.shape[0]

    # obtener el total de la base de datos
    row = database.get_all(Hired_employees)
    all_hired = []
    for hired in row:
        new_dept = {
            "id": hired.id,
        }

        all_hired.append(new_dept)
    
    max_sqlhired =  len(all_hired)

    if int(parm) <= max_hired:
        diff_hired = max_hired - max_sqlhired
        return diff_hired, max_hired
    else:
        return 0


################ funciones para validaciones de datos 
#####################################################

def validate_date(datetime_):
    try:
        d = datetime.fromisoformat(datetime_[:-1]).astimezone(timezone.utc)
        print(d.strftime('%Y-%m-%d %H:%M:%S'))                    
        return 1
    except ValueError:
        return 0

def validate_int(param):
    try:
        d = int(param)
        return 1
    except ValueError:
        return 0
