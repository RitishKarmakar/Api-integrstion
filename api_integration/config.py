class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "your-jwt-secret"
    MAIL_SERVER = "smtp.example.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "your-email@example.com"
    MAIL_PASSWORD = "your-email-password"
