from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '737A6058082AE0297CE9893822CBE175773851A82231728442282232F6DDA1E9'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db = SQLAlchemy(app)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(120), nullable=False)
    data_di_pubblicazione = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    testo = db.Column(db.Text, nullable=False)
    autori = db.Column(db.Text, nullable=False)
    testata_giornalistica = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.titolo}', '{self.data_di_pubblicazione}', '{self.autori}', '{self.testata_giornalistica}','{self.link}')"


with app.app_context():
    db.create_all()

    import feedparser
    import newspaper

    GOOGLE_RSS_URL="https://news.google.com/rss?hl=it&gl=IT&ceid=IT:it"
    NewsFeed = feedparser.parse(GOOGLE_RSS_URL)

    # NewsFeed = feedparser.parse(GOOGLE_RSS_KEYWORD_LOCALIZATION.replace("<KEYWORD>",keyword))
    newss=[]
    for newsItem in NewsFeed.entries:
        article=newspaper.Article(url=newsItem["link"])
        article.download()
        article.parse()
        # print(article.title+"\n"+article.text+"\n"+str(article.publish_date)+"\n"+"\n -----Nuovo Articolo------ \n")
        
        newss.append({"titolo":article.title,"autori":article.authors,"testata_giornalistica":newsItem.source["title"],"data_di_pubblicazione":article.publish_date,"link":newsItem["link"],"testo":article.text})
        


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home Page", news=newss)
if __name__ == '__main__':
    app.run(debug=True)
