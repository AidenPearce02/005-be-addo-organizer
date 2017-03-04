from datetime import date,datetime
from flask import Flask
from flask import g, request, redirect, url_for, render_template
from flask_login import LoginManager, current_user, login_user, logout_user

from models import User, Task, initialize_databases

app = Flask("TaskList")
app.secret_key = "super secret key"

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.get(id=int(id))


@app.route("/", methods=["GET"])
def index():
    today=datetime.now().date()
    return render_template("index.html",tasks=Task,today=today)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    registered_user = User.filter(User.username == username).first()

    if registered_user is None:
        return redirect(url_for("login"))  # redirect back to login page if can't wasn't found

    if not registered_user.password.check_password(password):
        return redirect(url_for("login"))  # redirect back to login page if incorrect password

    login_user(registered_user)
    return redirect(request.args.get("next") or url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/registration', methods=["GET", "POST"])
def registration():

    if request.method == "GET":
        return render_template("registration.html")

    username = request.form["username"]
    password = request.form["password"]

    User.create(username=username, password=password)

    return redirect(url_for("index"))


@app.route('/create', methods=["GET", "POST"])
def create():

    if request.method == "GET":
        return render_template("create.html")

    topic = request.form["topic"]
    task = request.form["task"]
    date = datetime.strptime(request.form["date"],'%d.%m.%Y').date()
    Task.create(username=g.user.username, topic=topic,task=task,date=date)

    return redirect(url_for("index"))


@app.route('/edit/task/<int:task_id>', methods=["GET", "POST"])
def edit(task_id):

    if request.method == "GET":
        return render_template("edit.html",task=Task.get(Task.id == task_id),task_id=task_id)

    topic = request.form["topic"]
    task = request.form["task"]
    date = request.form["date"]
    state = False
    if request.form.get('state') == "on":
        state = True
    q = Task.update(topic=topic, task=task, date=date, state=state).where(Task.id == task_id)
    q.execute()
    return redirect(url_for("index"))

if __name__ == "__main__":
    initialize_databases()
    app.run(use_reloader=True)
