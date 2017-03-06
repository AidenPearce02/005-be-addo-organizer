import peewee as pw
from playhouse.fields import PasswordField as pf
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, PasswordField, validators

db = pw.SqliteDatabase('database.db')


def initialize_databases():
    User.create_table(fail_silently=True)
    Task.create_table(fail_silently=True)
    try:
        User.create(
            username='root',
            password='123'
        )
    except pw.IntegrityError:
        pass


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = pw.CharField(max_length=70, unique=True)
    password = pf()
    state = pw.BooleanField(default=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.state

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Task(BaseModel):
    username = pw.CharField(max_length=70)
    topic = pw.CharField(max_length=70)
    task = pw.CharField(max_length=250)
    date = pw.DateField()
    state = pw.BooleanField(default=False)

    def is_active(self):
        return self.state

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Task %r>' % (self.topic)


class LARForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=3, max=25)
    ])


class EACForm(FlaskForm):
    topic = StringField('Topic', [validators.DataRequired(), validators.Length(max=25)])
    task = StringField('Task', [validators.Length(max=250)])
    date = DateField('Date', [validators.DataRequired()], format='%d.%m.%Y')
    state = BooleanField('Done')
