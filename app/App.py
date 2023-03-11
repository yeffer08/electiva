############# importar librerias o recursos#####
import os

from flask import Flask, request, jsonify,render_template,url_for , session,redirect
from flask_mysqldb import MySQL
from flask.helpers import flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_cors import CORS, cross_origin




# initializations
app = Flask(__name__)
CORS(app)




# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'baseDeDatos'
mysql = MySQL(app)

# settings A partir de ese momento Flask utilizará esta clave para poder cifrar la información de la cookie
app.secret_key = "mysecretkey"


@app.route('/index')
def index():
    return render_template('index.html')


# ruta para consultar todos los registros LISTO
@app.route('/getAll', methods=['GET'])
def getAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user')
        rv = cur.fetchall()

        cur.execute('SELECT * FROM profile')
        rl = cur.fetchall()
        cur.close()
        
        payload = []
        content = {}

        for result in rv:
            content = {'id': result[0], 'Usuario': result[1], 'contraseña': result[2], 'email': result[3], 'phone': result[4], 'perfilid': result[5]}
            payload.append(content)
            
        for result in rl:
            content = {'id': result[0], 'fullname': result[1], 'description': result[2]}
            payload.append(content)
            content = {}

        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


# ruta para consultar por parametro LISTO
@app.route('/getAllById/<id>',methods=['GET'])
def getAllById(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE id = %s', (id))
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'fullname': result[1], 'phone': result[2], 'email': result[3]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
    

#### ruta para crear un registro LISTO########
@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    try:
        if request.method == 'POST':
            nombrep = request.form['perfilname']
            description = request.form['Tipo']
            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO `profile` (`fullname`, `description`) VALUES ('{nombrep}','{description}')")
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion":"Registro exitoso"})
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM profile")
            row = cur.fetchall()
            cur.close()

            payload = []
            for result in row:
                content = {'id': result[0], 'fullname': result[1], 'description': result[2]}
                payload.append(content)

                
            return render_template('login.html',row=payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


######### ruta para actualizar################
@app.route('/update/<id>', methods=['PUT'])
def update_contact(id):
    try:
        fullname = request.json['fullname']
        description = request.json['phone']
        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE profile SET fullname = {0}, email = {1} WHERE id = {3} """.format(fullname, description, id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


@app.route('/delete/<id>', methods = ['DELETE'])
def delete_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM profile WHERE id = {0}'.format(id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
