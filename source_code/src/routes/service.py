import os
import math
from app import redis#, db
from flask import Blueprint, render_template, request, redirect, url_for, flash
#from redis import Redis
from models.emp import Departments, Jobs, Hired_employees, Log_action
from utils.funtions import session, jwt, datetime, timedelta, json, database, download_file_from_google_drive, pd, validate_load_hired, validate_date, validate_int
from os import getenv

service = Blueprint("service", __name__)

#redis = redis.Redis(host='redis', port=6379)

@service.route("/", methods=["POST"])
def index():
    return "Home"

@service.route("/login", methods=["POST"])
def login():
    #session = requests.Session()

    data = request.get_json()
    
    session['current_user'] = data['user']
    
    token = jwt.encode(payload={**data, "exp":datetime.utcnow() + timedelta(seconds=30)}, key=getenv("SECRET"), algorithm="HS256")
    
    if data['password'] == 1234:
        return token.encode("UTF-8")        
    else:
        return json.dumps("user not found"), 404

@service.route('/load_files')
#@token_required
def load_files():
    #redis.incr('hits')
    #return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')
    try:
        destination = r'\download\\'

        directory = os.path.abspath('.') 
        full_path = directory + destination 

        file_id = '1EETspcs5JiotdMxmK32naqVcz3dS03Qy' 

        download_file_from_google_drive(file_id, full_path, 'hired_employees.csv')

        return json.dumps("Csv cargados"), 405
    
    except NameError:
        print("NameError: error de carga.")
        return json.dumps("error carga"), 405

@service.route('/add_deparments', methods=['POST'])
def add_deparments():
    data = request.get_json()

    name_dept = data['departments']
    
    database.add_instance(Departments, departments=name_dept)

    return json.dumps("Added_departments"), 200

@service.route('/all_deparments', methods=['GET'])
#@token_required
def all_deparments():
    departments = database.get_all(Departments)
        
    all_dept = []
    for dept in departments:
        new_dept = {
            "id": dept.id,
            "departments": dept.departments            
        }

        all_dept.append(new_dept)
    return json.dumps(all_dept), 200

@service.route('/load_deparments', methods=['GET'])
#@token_required
def load_deparments():
    print("****cargando departments****")

    destination = r'\download\\'

    directory = os.path.abspath('.') 
    full_path = directory + destination 

    file_id_A = '1Z_iMmyJsxiDvr5T0KW9pXBrtqz96BrBG'
    
    download_file_from_google_drive(file_id_A, full_path, 'departments.csv')

    path_j = r'.\download\departments.csv'

    df = pd.read_csv(path_j,sep=',', names = ["id", "departments"], keep_default_na=False)
    
    for index, row in df.iterrows():
        print(row['departments'])

        str_validator = ''
        count_validator = 0
        
        ######################################## validaciones DEPARTMENTS ####################################                    
        if not isinstance(row['departments'], str):                     
            str_validator = str_validator + "departments invalido,"                     
            count_validator += 1

        if  count_validator == 0:  
            database.add_instance(Departments, departments=row['departments'])
        else:
            user_ = session['current_user']
            DateTime_ = datetime.now()
            DateTime_NOW =  DateTime_.isoformat(" ", "seconds")

            database.add_instance(Log_action,user=str(user_), action=str(str_validator), end_point=str("GET, /load_jobs/"),date_action=str(DateTime_NOW))    

    return json.dumps("departamento cargados"), 200

@service.route('/load_jobs', methods=['GET'])
#@token_required
def load_jobs():
    print("****cargando jobs****")

    destination = r'\download\\'

    directory = os.path.abspath('.') 
    full_path = directory + destination 

    file_id_B = '1806a7U-HTDSoIMycNOnw5ldC3Gud00li'

    download_file_from_google_drive(file_id_B, full_path, 'jobs.csv')

    path_j = r'.\download\jobs.csv'

    df = pd.read_csv(path_j,sep=',', names = ["id", "job"], keep_default_na=False)

    for index, row in df.iterrows():
        print(row['job'])

        str_validator = ''
        count_validator = 0
        ######################################## validaciones job ####################################                
    
        if not isinstance(row['job'], str):                     
            str_validator = str_validator + "job invalido,"                     
            count_validator += 1
        
        if  count_validator == 0:  
            database.add_instance(Jobs, job=row['job'])
        else:
            user_ = session['current_user']
            DateTime_ = datetime.now()
            DateTime_NOW =  DateTime_.isoformat(" ", "seconds")

            database.add_instance(Log_action,user=str(user_), action=str(str_validator), end_point=str("GET, /load_jobs/"),date_action=str(DateTime_NOW))    

    return json.dumps("Jobs cargados"), 200

@service.route('/load_hired/<row_count>', methods=['GET'])
#@token_required
def load_hired(row_count):
    
    #val_count = int(row_count)
    val_count = int(row_count) - 1

    #print("apuntador->",val_count)

    path_j = r'.\download\hired_employees.csv'
    
    df_ = pd.read_csv(path_j,sep=',', names = ["id_hired", "name", "date_time", "dept_id_", "job_id"], keep_default_na=False)

    #print(df_)    
    if validate_load_hired(val_count):
        diff_hired, max_hired = validate_load_hired(val_count)
        
        print("sql--input->",diff_hired,val_count)
        
        cont_hired = val_count # ingresar segun la entrada
        
        #print(df_)

        if val_count <= diff_hired:

            str_validator = ''

            for i in range(len(df_)):
                
                str_validator = ''

                count_validator = 0

                hired_id=df_.iloc[i,0]                
                name_=df_.iloc[i,1]                
                datetime_=df_.iloc[i,2]
                dept_id_=df_.iloc[i,3]
                job_id_=df_.iloc[i,4]
                #print("index->",i)

                ######################################## validaciones hired ####################################                
                if not validate_date(datetime_):
                    str_validator = str_validator + "Fecha invalida,"
                    count_validator += 1
                name_ = name_.split()
                if not isinstance(name_[0], str) and not isinstance(name_[1], str):                     
                    str_validator = str_validator + "nombre no invalido,"                     
                    count_validator += 1
                #if not isinstance(dept_id_, int):
                if not validate_int(dept_id_) or math.isnan(dept_id_):                
                    str_validator = str_validator + "deparmentid invalido," 
                    print(dept_id_)                     
                    count_validator += 1 
                if not validate_int(job_id_) or len(job_id_)==0:
                    str_validator = str_validator + "job_id invalido,"
                    print("job-valor",len(job_id_))
                    count_validator += 1 

                exist_ = Hired_employees.query.filter_by(id_hired=int(hired_id)).first() #asegurar solo los no existan
                
                if not exist_:
                    if  count_validator == 0:  
                        
                        name_v = str(name_)[1:-1] 

                        database.add_instance(Hired_employees,name=str(name_v), datetime=str(datetime_), department_id=int(dept_id_), job_id=int(job_id_), id_hired=int(hired_id))    
                        cont_hired -=1            
                        print("count_hired->",cont_hired)                    
                    else:
                        user_ = session['current_user']
                        DateTime_ = datetime.now()
                        DateTime_NOW =  DateTime_.isoformat(" ", "seconds")

                        database.add_instance(Log_action,user=str(user_), action=str(str_validator), end_point=str("GET, /total_hired/"),date_action=str(DateTime_NOW))    

                if cont_hired == 0:
                    break
                    
            return json.dumps("Added_add"), 200                                
        else:
            return json.dumps("Added_exceeded"), 405

