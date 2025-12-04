from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# -----------------------------
# Configurações básicas
# -----------------------------
load_dotenv('.env')

app = Flask(__name__)

# Configurações do Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-padrao-secreta')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -----------------------------
# Extensões
# -----------------------------
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'  # nome da rota de login
bcrypt = Bcrypt(app)

# -----------------------------
# Configuração de upload (se quiser usar futuramente)
# -----------------------------
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -----------------------------
# Importa as rotas e modelos
# -----------------------------
from app import view, models
