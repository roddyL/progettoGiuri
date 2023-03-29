from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import requests
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required

API_KEY = "4b362c42052d41a7a8541e6f350b1004"





app = Flask(__name__)
app.config['SECRET_KEY'] = '737A6058082AE0297CE9893822CBE175773851A82231728442282232F6DDA1E9'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations_db.db'
registrations_db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)



class User(registrations_db.Model):
    __tablename__ = "User"
    id = registrations_db.Column(registrations_db.Integer, primary_key=True)
    email = registrations_db.Column(registrations_db.String(120), unique=True, nullable=False)
    password = registrations_db.Column(registrations_db.String(50), nullable=False)

    def __repr__(self):
        return f"User('{self.email}')"

class NewsDb(registrations_db.Model):
    __tablename__ = "NewsDb"
    id = registrations_db.Column(registrations_db.Integer, primary_key=True)
    email = registrations_db.Column(ForeignKey("User.email"))
    data = registrations_db.Column(registrations_db.String(5000), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.email}', '{self.data}')"


with app.app_context():
    registrations_db.create_all()

def userNews():
    pass

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error_message = 'Email already exists!'
            return render_template('registration.html', error_message=error_message)
        else:
            new_user = User(email=email, password=password)
            registrations_db.session.add(new_user)
            registrations_db.session.commit()
            return redirect(url_for('login'))
    else:
        return render_template('registration.html')

'''@app.route("/registration", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(password=pw_hash,
                    email=form.email.data)
        with app.app_context():

            registrations_db.session.add(user)
            registrations_db.session.commit()

        flash(
            f"Your account has been created {form.username.data}", category="success")
        return redirect('/login')

    return render_template("registration.html", title="Register Page", form=form)'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is not None and user.password == password:
            session['user_id'] = user.id
            return render_template('index.html')
        else:
            error_message = 'Invalid email or password'
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

'''@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        candidate = form.password.data
        if user and bcrypt.check_password_hash(user.password, candidate):
            login_user(user, remember=form.remember_me.data)
            flash('Welcome', category='success')
            return redirect('index')

        else:
            flash('Wrong emil or password', category='danger')
            return redirect('login')
    else:
        return render_template("login.html", title="Login Page", form=form)'''


@app.route("/logout")
def logout():
    if session["user_id"]:
        session.clear()
    # flash(f'Logged Out', category='info')
    return redirect('/index')







@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user is not None:
            return render_template('index.html', user=user)
    return redirect(url_for('login'))



# class News(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     titolo = db.Column(db.String(120), nullable=False)
#     data_di_pubblicazione = db.Column(db.DateTime, nullable=False,
#                             default=datetime.utcnow)
#     testo = db.Column(db.Text, nullable=False)
#     autori = db.Column(db.Text, nullable=False)
#     testata_giornalistica = db.Column(db.Text, nullable=False)
#     link = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f"Post('{self.id}', '{self.titolo}', '{self.data_di_pubblicazione}', '{self.autori}', '{self.testata_giornalistica}','{self.link}')"


with app.app_context():
    db.create_all()



@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html", title="Home Page")

@app.route("/news", methods=['POST'])
def news():
    user_keyword=request.form.get('search_topic')

@app.route("/favourites", methods=['POST'])
def favourites():
    if session["user_id"]:
        return render_template("news.html", title="News", newss=userNews())
    
    


if __name__ == '__main__':
    app.run(debug=True)


