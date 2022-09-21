# Flask-Docker-MySQL: 

proyecto de prueba que usa base de mysql local y docker

# Empezando:

**Paso 2**: Clona el proyecto en tu maquina local usando el siguiente comando

git clone https://github.com/carlgm12/emp_hired.git

# Prerequisites

**Git**

**Paso 1**:Asegurarce de tener docker instalado puede ubicarlo en el siguiente link:

https://git-scm.com/downloads

**Docker**

**Paso 2**:Asegurarce de tener docker instalado puede ubicarlo en el siguiente link:

https://www.docker.com/

**Xampp**:

**Paso 3**: Instalar una base de datos local para el proyecto con Xampp atraves del siguiente link:

https://www.apachefriends.org/download.html

# Instalacion:

**Paso 1**: Activar el entorno local que esta en la carpeta /env en su consola de comandos

source_code/env/Scripts/activate.bat

**Paso 2**: Activar el mysql atravez de la consola de comandos de xampp.

**Paso 3**: migrar la base de datos atravez de los siguientes en la consola comando del proyecto comandos:

**Set FLASK_APP=index.py
**Flask db init
**flask db migrate
**Flask db upgrade

**Paso 4**: Correr el siguiente comando en la carpeta raiz de tu proyecto usando la linea de comando

docker-compose up --build

**Paso 5**: Ejecutar el siguiente comando para poner el marcha en la carpeta raiz del mismo el proyecto:

/src/python index.py

**Paso 6**: Habrir en el navegador la siguiente url

http://localhost:5000/

