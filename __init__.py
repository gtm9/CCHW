from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"




@app.route('/index', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            # return redirect(url_for('login'))
            return redirect(url_for('login', fn=user.f_name,ln=user.l_name))
    else:
        return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        pusername = request.form['username']
        pfirst = request.form['first']
        plast = request.form['last']
        pemail = request.form['email']
        ppassword = request.form['password']

        u = User(username=pusername, f_name=pfirst,l_name=plast,email=pemail,password=ppassword)
        db.session.add(u)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('register.html')


@app.route('/login/<string:fn>/<string:ln>', methods=['GET','POST'])
def login(fn,ln):
    return  render_template('login.html', fn=fn, ln=ln)






# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.route('/index')
# def index()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "User ('" + str(self.username) + ", '" + str(self.email) + "')"