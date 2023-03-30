from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import ForeignKey
import ast
from utils.functions import news_get

app = Flask(__name__)
app.config['SECRET_KEY'] = '737A6058082AE0297CE9893822CBE175773851A82231728442282232F6DDA1E9'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations_db.db'
registrations_db = SQLAlchemy(app)


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
    user_id = registrations_db.Column(ForeignKey("User.id"))
    url = registrations_db.Column(registrations_db.String(100), nullable=False)
    data = registrations_db.Column(registrations_db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.user_id}', '{self.url}', '{self.data}')"


with app.app_context():
    registrations_db.create_all()


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
            session['user_id'] = new_user.id

            return render_template('index.html')
    else:
        return render_template('registration.html')


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


@app.route("/logout")
def logout():
    if session["user_id"]:
        session.clear()
    return redirect('/index')


@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html", title="Home Page")


@app.route('/add_remove_fav', methods=['POST',"DELETE"])
def add_remove_fav():
    data = request.get_json(force=True)
    url = ast.literal_eval(data)["url"]

    if request.method=="POST":
        if not NewsDb.query.filter_by(user_id=int(session["user_id"]),url=url).first():
            news_db = NewsDb(user_id=int(session["user_id"]),url=url, data=data)
            registrations_db.session.add(news_db)
            registrations_db.session.commit()
    elif request.method=="DELETE":
        if NewsDb.query.filter_by(user_id=int(session["user_id"]),url=url).delete():
            registrations_db.session.commit()
    return json.dumps({'status':'OK'})


@app.route("/news", methods=['POST'])
def news():
    user_keyword=request.form.get('search_topic')
    newss=news_get(user_keyword)
    for i in range(len(newss)):
        if newss[i]['author']:
            newss[i]['author'] = newss[i]['author'][:10]
            newss[i]['publishedAt'] = newss[i]['publishedAt'].replace('T', ' ')[:16]

    return render_template("news.html", title="News", newss=newss)


@app.route("/favourite")
def favourite():
    query_result = NewsDb.query.filter_by(user_id=int(session["user_id"])).with_entities(NewsDb.data).all()
    articles_result = [ast.literal_eval(article[0]) for article in query_result]

    return render_template("favourite.html", title="favourite", newss=articles_result)


if __name__ == '__main__':
    app.run(debug=True)


