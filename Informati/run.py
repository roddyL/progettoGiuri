from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import requests
API_KEY = "4b362c42052d41a7a8541e6f350b1004"

def news_get(keyword):
    url = f"https://newsapi.org/v2/everything?language=it&q={keyword}&apiKey={API_KEY}"
    response = requests.get(url)
    return json.loads(response.text)["articles"]

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

if __name__ == '__main__':
    app.run(debug=True)






# def get_data():
#     with open('data.json') as json_file:
#         data = json.load(json_file)