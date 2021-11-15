# SE IMPORTAN LAS LIBRERIAS
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt

# CREA EL OBJETO DEL FLASK
app = Flask(__name__)

# ESTABELCE LA LLAVE SECRETA
app.secret_key = "appLogin"

# CONFIGURA
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbpos'

# CREA EL OBJETO MYSQL
mysql = MySQL(app)

# SEMILLA PARA ENCRIPTAMIENTO
semila = bcrypt.gensalt()

# DEFINE LA RUTA PRINCIPAL


@app.route("/")
# DEFINE LA FUNCION PRINCIPAL
def main():
    if 'nombre' in session:
        # CARGA TEMPLATE main.html
        return render_template('menu.html')
    else:
        # CARGA TEMPLATE main.html
        return render_template('login.html')

# DEFINE LA RUTA DE INDEX


@app.route("/menu")
# DEFINE LA FUNCION PRINCIPAL
def inicio():
    # VERIFICA QUE HAYA SESSION
    if 'nombre' in session:
        # CARGA TEMPLATE main.html
        return render_template('menu.html')
    else:
        # CARGA TEMPLATE main.html
        return render_template('login.html')

# DEFINE LA RUTA DE REGISTRO


@app.route("/registrar", methods=["GET", "POST"])
# FUNCION PARA REGISTAR
def registrar():
    if (request.method == "GET"):
        # VERIFICA QUE HAYAS SESION
        if 'nombre' in session:
            # CARGA TEMPLATE main.html
            return render_template('menu.html')
        else:
            # ACCESO NO CONCEDIDO
            return render_template("login.html")
    else:
        # OBTIENE LOS DATOS
        nombre = request.form['nmNombreRegistro']
        correo = request.form['nmCorreoResgistro']
        password = request.form['nmPasswordRegistro']
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semila)
        print("Insertando")
        print("Paswwor encode  :", password_encode)
        print("Paswword_encriptado:", password_encriptado)

        # PREPARA EL QUERY PARA INSERCION
        sQuery = "INSERT into Login (correo, password, nombre) VALUES (%s, %s, %s)"

        # CREA EL CURSOR PARA EJECUCION
        cur = mysql.connection.cursor()

        # EJECUTA LA SENTENCIA
        cur.execute(sQuery, (correo, password_encriptado, nombre))

        # EJECUTA EL COMMIT
        mysql.connection.commit()

        # REGISTRA LA SESSION
        session['nombre'] = nombre
        #session['correo'] = correo

        # REDIRIGE A INDEX
        return redirect(url_for('menu'))

# DEFINE LA RUTA A INGRESAR


@app.route("/ingresar", methods=["GET", "POST"])
# FUNCION PARA REGISTRAR
def ingresar():
    if (request.method == "GET"):
        if 'nombre' in session:
            # CARGA TEMPLATE main.html
            return render_template('menu.html')
        else:
            # ACCESO NO CONCEDIDO
            return render_template("login.html")
    else:
        # OBTIENE LOS DATOS
        correo = request.form['nmCorreoResgistro']
        password = request.form['nmPasswordRegistro']
        password_encode = password.encode("utf-8")

        # CREA EL CURSOR PARA EJECUCION
        cur = mysql.connection.cursor()

        # PREPARA EL QUERY PARA LA CONSULTA
        sQuery = "SELECT correo, password, nombre FROM Login WHERE correo = $s"

        # EJECUTA LA SENTENCIA
        cur.execute(sQuery, [correo])

        # OBTENGO EL DATO
        usuario = cur.fetchone()

        # CIERRO LA CONSULTA
        cur.close()

        # VERIFICAR SI OBTUVO EL DATO
        if (usuario != None):

            # OBTIENE EL PASWSWORD ENCRIPDATO ENCODE
            password_encriptado_encode = usuario[1].encode()
            # VERIFICA EL PASSWORD
            if (bcrypt.checkpw(password_encode, password_encriptado_encode)):
                # REGISTRA LA SESSION
                session['nombre'] = usuario[2]
                # REDIRIGE A INDEX
                # return render_template('menu.html')
                return redirect(url_for('menu'))
            else:
                # MENSAJE FLASH
                flash("El password no es correcto", "alert-warning")

                # REDIRIGE A INGRESAR
                return render_template('login.html')

        else:
            # MENSAJE FLASH
            flash("El correo no existe", "alert-warning")

            # REDIRIGE A LOGIN
            return render_template('login.html')

# DEFINE LA RUTA DE SALIDA


@app.route("/salir")
# FUNCION PARA SALIR
def salir():
    # LIMPIA LA SESIONES
    session.clear()

    # MANDA A INGRESAR
    return redirect(url_for('login'))


# FUNCION PRINCIPAL
if __name__ == '__main__':

    # EJECUTA EL SERVIDOR EN DEBUG
    app.run(debug=True)
