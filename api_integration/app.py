from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail
from routes.auth import auth_bp

# Initialize Flask
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db = SQLAlchemy(app)
Session(app)
mail = Mail(app)

# Register blueprints
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return render_template('index.html')
