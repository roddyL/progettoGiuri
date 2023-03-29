from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import regex as re
import wordcloud
import nltk

API_KEY = "4b362c42052d41a7a8541e6f350b1004"

def news_get1(keyword):
    url = f"https://newsapi.org/v2/everything?language=it&q={keyword}&apiKey={API_KEY}"
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



app = Flask(__name__)
app.config['SECRET_KEY'] = '737A6058082AE0297CE9893822CBE175773851A82231728442282232F6DDA1E9'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db = SQLAlchemy(app)


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
def home():
    return render_template("index.html", title="Home Page")

@app.route("/news", methods=['POST'])
def news():
    user_keyword=request.form.get('search_topic')
    return render_template("news.html", title="News", newss=news_get(user_keyword))

@app.route('/add_remove_fav', methods=['POST'])
def add_remove_fav():
    print("AJAXO")

    data =request.form['dic']
    dml = request.form['dml']

    if dml == 'true':
        print("INSERT")
        print(data)
        # db.session.add(data)
        # db.session.commit()
    else:
        print("DELETE")
        print(data)
        # db.session.delete(data)
        # db.session.commit()

    return json.dumps({'status':'OK'});



if __name__ == '__main__':
    app.run(debug=True)







# def get_data():
#     with open('data.json') as json_file:
#         data = json.load(json_file)