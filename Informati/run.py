from datetime import datetime
import re

from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import ForeignKey, create_engine, delete, text
import wordcloud
import nltk
API_KEY = "4b362c42052d41a7a8541e6f350b1004"





app = Flask(__name__)
app.config['SECRET_KEY'] = '737A6058082AE0297CE9893822CBE175773851A82231728442282232F6DDA1E9'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations_db.db'
registrations_db = SQLAlchemy(app)
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


def news_get1(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}"
    response = requests.get(url)
    response =json.loads(response.text)["articles"]


        # with open('sample.json', 'r') as openfile:
        # # Reading from json file
        #     response = json.load(openfile)
    testo_completo= ""
    for article in response:
        testo_completo+=article["content"]
        testo_completo+=article["title"]

    testo_completo = re.sub("\[([^\]]+)\]"," ",testo_completo)
    testo_completo


    text = testo_completo
    text = nltk.word_tokenize(text, language="italian")
    result = nltk.pos_tag(text)

    new_text = ' '.join([word for word, tag in result if tag[0] in "NJV"])

    stopwords = set(wordcloud.STOPWORDS)
    stopwords.update([keyword,'ad', 'al', 'https','allo', 'ai','furono', 'fossi', 'fosse', 'fossimo', 'fossero', 'essendo', 'faccio', 'fai', 'facciamo',
    'fanno', 'faccia', 'facciate', 'facciano', 'farò', 'farai', 'farà', 'faremo', 'farete', 'faranno', 'farei', 'faresti', 'farebbe',
    'faremmo', 'fareste', 'farebbero', 'facevo', 'facevi', 'faceva', 'facevamo', 'facevate', 'facevano', 'feci', 'facesti', 'fece',
    'facemmo', 'faceste', 'fecero', 'facessi', 'facesse', 'facessimo', 'facessero', 'facendo', 'sto', 'stai', 'sta', 'stiamo',
    'stanno', 'stia', 'stiate', 'stiano', 'starò', 'starai', 'starà', 'staremo', 'starete', 'staranno', 'starei', 'staresti',
    'starebbe', 'staremmo', 'stareste', 'starebbero', 'stavo', 'stavi', 'stava', 'stavamo', 'stavate', 'stavano', 'stetti',
    'stesti', 'stette', 'stemmo', 'steste', 'stettero', 'stessi', 'stesse', 'stessimo', 'stessero', 'stando' 'agli', 'all',
    'agl', 'alla', 'alle', 'con', 'col', 'coi', 'da', 'dal', 'dallo', 'dai', 'dagli', 'dall', 'dagl', 'dalla', 'dalle',
    'di', 'del', 'dello', 'dei', 'degli', 'dell', 'degl', 'della', 'delle', 'in', 'nel', 'nello', 'nei', 'negli', 'nell',
    'negl', 'nella', 'nelle', 'su', 'sul', 'sullo', 'sui', 'sugli', 'sull', 'sugl', 'sulla', 'sulle', 'per', 'tra', 'contro',
    'io', 'tu', 'lui', 'lei', 'noi', 'voi', 'loro', 'mio', 'mia', 'miei', 'mie', 'tuo', 'tua', 'tuoi', 'tue', 'suo', 'sua',
    'suoi', 'sue', 'nostro', 'nostra', 'nostri', 'nostre', 'vostro', 'vostra', 'vostri', 'vostre', 'mi', 'ti', 'ci', 'vi',
    'lo', 'la', 'li', 'le', 'gli', 'ne', 'il', 'un', 'uno', 'una', 'ma', 'ed', 'se', 'perché', 'anche', 'come', 'dov',
    'dove', 'che', 'chi', 'cui', 'non', 'più', 'quale', 'quanto', 'quanti', 'quanta', 'quante', 'quello', 'quelli',
    'quella', 'quelle', 'questo', 'questi', 'questa', 'queste', 'si', 'tutto', 'tutti', 'a', 'c', 'e', 'i', 'l',
    'o', 'ho', 'hai', 'ha', 'abbiamo', 'avete', 'hanno', 'abbia', 'abbiate', 'abbiano', 'avrò', 'avrai', 'avrà', 'avremo',
    'avrete', 'avranno', 'avrei', 'avresti', 'avrebbe', 'avremmo', 'avreste', 'avrebbero', 'avevo', 'avevi', 'aveva',
    'avevamo', 'avevate', 'avevano', 'ebbi', 'avesti', 'ebbe', 'avemmo', 'aveste', 'ebbero', 'avessi', 'avesse',
    'avessimo', 'avessero', 'avendo', 'avuto', 'avuta', 'avuti', 'avute', 'sono', 'sei', 'è', 'siamo', 'siete',
    'sia', 'siate', 'siano', 'sarò', 'sarai', 'sarà', 'saremo', 'sarete', 'saranno', 'sarei', 'saresti',
    'sarebbe', 'saremmo', 'sareste', 'sarebbero', 'ero', 'eri', 'era', 'eravamo', 'eravate', 'erano', 'fui',
    'fosti', 'fu', 'fummo', 'foste', 'iframe','class','src',
    "più","l","non","dalla","nell","o","alla","nella","nel","si","al","dal","ha","è","e","un","una","uno","che","il", "lo", "la", "i", "gli", "le", "di", "da",
      "del", "dello", "della", "dei", "degli", "delle", "in", "a", "con", "su", "per", "tra", "fra"])

    modello = wordcloud.WordCloud(stopwords=stopwords,width=1920, height=1080, background_color="rgba(255, 255, 255, 0)").generate(new_text)
    modello.to_file("./static/nuvola.png")

    return response #return json.loads(response.text)["articles"

def news_get(keyword):
    with open('sample.json', 'r') as openfile:
        # Reading from json file
            response = json.load(openfile)
    return response


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
    # flash(f'Logged Out', category='info')
    return redirect('/index')



@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html", title="Home Page")

@app.route('/add_remove_fav', methods=['POST'])
def add_remove_fav():
    print("AJAXO")
    data = request.get_json()
    print(type(data))
    data_json = data

    url = str(data_json["url"])

    print(data)


    if request.method=="POST":
        print("INSERT")
        # print(data)
        if not NewsDb.query.filter_by(user_id=int(session["user_id"]),url=url).first():
            news_db = NewsDb(user_id=int(session["user_id"]),url=url, data=data)
            registrations_db.session.add(news_db)
            registrations_db.session.commit()
    elif request.method=="DELETE":
        print("DELETE")
        # print(data)
        if NewsDb.query.filter_by(user_id=int(session["user_id"]),url=url).delete():
            registrations_db.session.commit()

    # data =request.form['dic']
    # dml = request.form['dml']

    # print(data)
    # data_json = json.loads(data.replace("'", "1234").replace("\"","'").replace("1234","\""))
    # print(data)

    # url = str(data_json["url"])
    # if dml == 'true':
    #     print("INSERT")
    #     # print(data)
    #     if not NewsDb.query.filter_by(user_id=int(session["user_id"]),url=url).first():
    #         news_db = NewsDb(user_id=int(session["user_id"]),url=url, data=data)
    #         registrations_db.session.add(news_db)
    #         registrations_db.session.commit()
    # else:
    #     print("DELETE")
    #     # print(data)
    #     if NewsDb.query.filter_by(user_id=int(session["user_id"]),url=url).delete():
    #         registrations_db.session.commit()
    return json.dumps({'status':'OK'})

@app.route("/news", methods=['POST'])
def news():
    user_keyword=request.form.get('search_topic')
    newss=news_get(user_keyword)
    for i in range(len(newss)):
        if newss[i]['author']:
            newss[i]['author'] = newss[i]['author'][:10]
            newss[i]['publishedAt'] = newss[i]['publishedAt'].replace('T', ' ')[:16]
    # print(newss)
    return render_template("news.html", title="News", newss=newss)



@app.route("/favourite")
def favourite():
    print("favourite")
    # engine = create_engine(r'sqlite:///.\instance\registrations_db.db')
    # conn = engine.connect()
    # result = conn.execute(text(f"SELECT data FROM NewsDb WHERE user_id = {int(session['user_id'])}"))
    # result = result.fetchall()
    
    # conn.close()
    # json_result =result[0][0]
    # json_result =json.loads(result[0][0].replace("'", "1234").replace("\"","'").replace("1234","\""))
    # print(type(json_result))




    # [user.serialize() for user in users]
    # print([article[0] for article in NewsDb.query.filter_by(user_id=int(session["user_id"])).with_entities(NewsDb.data).all()])
    # print([article for article in NewsDb.query.filter_by(user_id=int(session["user_id"])).with_entities(NewsDb.data).all()])
    result = [json.loads(article[0].replace("'", "1234").replace("\"","'").replace("1234","\"")) for article in NewsDb.query.filter_by(user_id=int(session["user_id"])).with_entities(NewsDb.data).all()]
    # json_result = json.dumps(result, cls=AlchemyEncoder)
    print(result)
    # prova = jsonify([article[0] for article in NewsDb.query.filter_by(user_id=int(session["user_id"])).with_entities(NewsDb.data).all()])
    return render_template("favourite.html", title="favourite", newss=result)

    
    


if __name__ == '__main__':
    app.run(debug=True)


