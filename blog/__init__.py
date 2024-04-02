from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from .constants import SQLALCHEMY_DATABASE_URI, APP_SECRET_KEY, EMAIL_PASS, EMAIL_USER

app=Flask(__name__)
app.secret_key=APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db=SQLAlchemy(app)
with app.app_context():
    db.create_all()
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='lform'#route function of login
login_manager.login_message_category='info'#bootstrap class
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=EMAIL_USER
app.config['MAIL_PASSWORD']=EMAIL_PASS
app.config['MAIL_AUTHENTICATION']='plain'
mail=Mail(app)


from blog import route