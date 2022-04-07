import json
from flask import Flask, request
from flaskext.mysql import MySQL
app = Flask (__name__)

#realizaremos la conexion a la BASE DE DATOS
app.config['MYSQL_DATABASE_HOST']='192.168.133.4'
app.config['MYSQL_DATABASE_PORT']= 3306
app.config['MYSQL_DATABASE_USER']='salvador g'
app.config['MYSQL_DATABASE_PASSWORD']='tolito123'
app.config['MYSQL_DATABASE_BD']='BIBLIOTECA'

mysql = MySQL()
mysql.init_app(app)

@app.get('/')
def hola():
    print(mysql.get_db().cursor())
    return "hola mundo"

@app.get('/libros')
def index():
    cursor = mysql.get_db().cursor()
    
    cursor.execute('''
    SELECT  nombre FROM BIBLIOTECA.Libros

    ''')
    libros=cursor.fetchall()

    libros_str = str(json.dumps(libros)).replace("[","").replace("]","").replace('"',"")

    return libros_str
#-------------------------------------------------------------
@app.get('/registro')
def modificar():

    codigobarras=request.args.get("codigobarras")
    nombre=request.args.get("nombre")
    autor=request.args.get("autor")
    genero=request.args.get("genero")
    editorial=request.args.get("editorial")
    estado=request.args.get("estado")
    imagen=request.args.get("imagen")
    existencias=request.args.get("existencias")

    print(estado)
    if not estado:
        return "parametros incompletos",400
    
    cursor = mysql.get_db().cursor()

    cursor.execute('''
          INSERT INTO BIBLIOTECA.Libros(codigobarras,nombre,autor,genero,editorial,estado,imagen,existencias)
          VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)
        ''',(codigobarras,nombre,autor,genero,editorial,estado,imagen,existencias))
    mysql.get_db().commit()

    return "datos modificados"
