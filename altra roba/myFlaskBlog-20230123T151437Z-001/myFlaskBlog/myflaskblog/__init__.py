
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from myflaskblog import routes

# creazione dell'applicazione flask
app = Flask(__name__)
# configurazione della chiave di cifratura per criptare lo scambio di dati tra utente e server
app.config['SECRET_KEY'] = '393D9DA176BE7B81874CED846EA9A3AFC2B9FE301DDAE7BA4284528B4735550A'
# uri per la connessione al database. In questo caso il database si chiama mydb
# Occhio al triplo slash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

# instanzio un oggetto sqlalchemy alla connessione del database
db = SQLAlchemy(app)
# instanzio un oggetto bcrypt per la crittografia dell'app
bcrypt = Bcrypt(app)
# instanzio un oggetto loginmanager per gestire le fasi di login dell'utente
login_manager = LoginManager(app)

# Inizializziamo tutte le tabelle presenti nel db
with app.app_context():
    db.create_all()
