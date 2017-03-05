from datetime import datetime
from flask import Flask
from flask import g, request, redirect, url_for, render_template,flash
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_bootstrap import Bootstrap

from models import LARForm, EACForm, User, Task, initialize_databases

app = Flask("TaskList")
Bootstrap(app   )
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
    form = LARForm()
    if request.method == 'POST':
        registered_user = User.filter(User.username == form.username.data).first()
        if registered_user is None:
            flash('Username is not found')
            return redirect(url_for("login"))  # redirect back to login page if can't wasn't found
        if not registered_user.password.check_password(form.password.data):
            flash('Password is wrong')
            return redirect(url_for("login"))  # redirect back to login page if incorrect password
        login_user(registered_user)
        flash('Login completed successfully')
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/registration', methods=["GET", "POST"])
def registration():
    form = LARForm()
    if request.method == 'POST':
        registered_user = User.filter(User.username == form.username.data).first()
        if registered_user is not None:
            flash('Username was used')
            return redirect(url_for("registration"))
        User.create(username=form.username.data,password=form.password.data)
        flash('Registration completed successfully')
        return redirect(url_for("index"))
    return render_template("registration.html", form=form)


@app.route('/create', methods=["GET", "POST"])
def create():
    form = EACForm()
    if request.method == "POST":
        Task.create(username=g.user.username, topic=form.topic.data, task=form.task.data, date=form.date.data)
        flash('Task created successfully')
        return redirect(url_for("index"))
    return render_template("create.html",form=form)


@app.route('/delete/task/<int:task_id>', methods=["GET"])
def delete(task_id):
    q = Task.delete().where(Task.id == task_id)
    q.execute()
    return redirect(url_for("index"))


@app.route('/edit/task/<int:task_id>', methods=["GET", "POST"])
def edit(task_id):
    form = EACForm()
    if request.method == "POST":
        q = Task.update(topic=form.topic.data, task=form.task.data, date=form.date.data, state=form.state.data).where(Task.id == task_id)
        q.execute()
        flash('Task edited successfully')
        return redirect(url_for("index"))
    task = Task.get(Task.id == task_id)
    form.topic.data = task.topic
    form.task.data = task.task
    form.date.data = task.date
    form.state.data = task.state
    return render_template("edit.html",form=form,task_id=task_id)

if __name__ == "__main__":
    initialize_databases()
    app.run(use_reloader=True)
