import peewee as pw
from playhouse.fields import PasswordField


dbU = pw.SqliteDatabase('databaseU.db')
dbT = pw.SqliteDatabase('databaseT.db')


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


class BaseModelU(pw.Model):
    class Meta:
        database = dbU


class User(BaseModelU):
    username = pw.CharField(max_length=70, unique=True)
    password = PasswordField()
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


class BaseModelT(pw.Model):
    class Meta:
        database = dbT


class Task(BaseModelT):
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

