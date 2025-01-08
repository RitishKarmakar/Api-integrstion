from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from routes.auth import auth_bp
from routes.landing_page import landing_bp
from routes.payment import payment_bp

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(landing_bp, url_prefix="/api/landing")
app.register_blueprint(payment_bp, url_prefix="/api/payment")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
