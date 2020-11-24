from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///cars.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Ingrese un nombre de usuario valido", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("ingrese una contraseña correcta", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalido nombre de usuario o contraseña", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        #si el usuario existe
        u=db.execute("select username from users where username=:user",user=request.form.get("username"))


        #si no coincide la contra y confirmation
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("contraseñas no coinciden",400)
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Escriba un nombre se usuario", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Ingrese una contraseña", 400)

        if not u:
            rows = db.execute("insert into users (username,hash) values (:username,:password)",
                          username=request.form.get("username"),password=generate_password_hash(request.form.get("password")))
            flash("Registrado")
        else:
            return apology("lo siento el usuario ya existe")

        register=rows
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/ventas")
def ventas():
    rows=db.execute("select * from ventas")

    return render_template("ventas.html",rows=rows)

@app.route("/inventario")
def inventario():
    rows=db.execute("select * from inventario")

    return render_template("inventario.html",rows=rows)

@app.route("/clientes")
def clientes():
    rows=db.execute("select * from clientes")

    return render_template("clientes.html",rows=rows)

@app.route("/proveedores")
def proveedores():
    rows=db.execute("select * from proveedor")

    return render_template("proveedores.html",rows=rows)

@app.route("/ml")
def ml():


    return render_template("ml.html")


@app.route("/rventas", methods=["GET", "POST"])
def rventas():
    if request.method == "POST":
        rows=db.execute("insert into ventas (modelo,marca,precio,fechaventa,kilometraje,temporada) values (:modelo,:marca,:precio,:fechaventa,:kilometraje,:temporada)",
                          modelo=request.form.get("modelo"),marca=request.form.get("marca"),precio=request.form.get("precio"),fechaventa=request.form.get("fechaventa"),kilometraje=request.form.get("kilometraje"),temporada=request.form.get("temporada"))

        rclientes=rows
        # Redirect user to home page
        return render_template("rventas.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("rventas.html")


@app.route("/rinv", methods=["GET", "POST"])
def rinv():
    if request.method == "POST":
        rows=db.execute("insert into inventario (modelo,marca,precio,fechaventa,proveedor,nombreC,cantidad) values (:modelo,:marca,:precio,:fechaventa,:proveedor,:nombreC,:cantidad)",
                          modelo=request.form.get("modelo"),marca=request.form.get("marca"),precio=request.form.get("precio"),fechaventa=request.form.get("fechaventa"),proveedor=request.form.get("proveedor"),nombreC=request.form.get("nombreC"),cantidad=request.form.get("cantidad"))

        rclientes=rows
        # Redirect user to home page
        return render_template("rinv.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        proveedor=db.execute("select nombre from proveedor")
        return render_template("rinv.html",proveedor=proveedor)

@app.route("/rclientes", methods=["GET", "POST"])
def rclientes():
    if request.method == "POST":
        rows=db.execute("insert into clientes (nombre,numero,direccion) values (:nombre,:numero,:direccion)",
                          nombre=request.form.get("nombre"),numero=request.form.get("numero"),direccion=request.form.get("direccion"))

        rclientes=rows
        # Redirect user to home page
        return render_template("rclientes.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("rclientes.html")
@app.route("/rprov", methods=["GET", "POST"])
def rprov():
    if request.method == "POST":
        rows=db.execute("insert into proveedor (nombre,correo,ntel) values (:nombre,:correo,:ntel)",
                          nombre=request.form.get("nombre"),correo=request.form.get("correo"),ntel=request.form.get("ntel"))

        rclientes=rows
        # Redirect user to home page
        return render_template("rprov.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("rprov.html")


@app.route("/uinventario", methods=["GET","POST"])
def uinventario():
    if request.method=="GET":
        rows=db.execute("select * from inventario")
        return render_template("uinventario.html",rows=rows)
    elif request.method=="POST":
        if request.form["id"]:
            db.execute("DELETE FROM inventario where id=:id",id=request.form["id"])
        return redirect(url_for("inventario"))

@app.route("/uprov", methods=["GET","POST"])
def uprov():
    if request.method=="GET":
        rows=db.execute("select * from proveedor")
        return render_template("uprov.html",rows=rows)
    elif request.method=="POST":
        if request.form["id"]:
            db.execute("DELETE FROM proveedor where id=:id",id=request.form["id"])
        return redirect(url_for("proveedores"))

@app.route("/uclientes", methods=["GET","POST"])
def uclientes():
    if request.method=="GET":
        rows=db.execute("select * from clientes")
        return render_template("uclientes.html",rows=rows)
    elif request.method=="POST":
        if request.form["id"]:
            db.execute("DELETE FROM clientes where id=:id",id=request.form["id"])
        return redirect(url_for("clientes"))

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
