import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mynew.db') #os.environ.get('MY_SQLALCHEMY_DATABASE_URI')
APP_SECRET_KEY = 'rishabh' #os.environ.get('APP_SECRET_KEY')
EMAIL_USER = 'pndtrishabh91@gmail.com' #os.environ.get('EMAIL_USER')
EMAIL_PASS = 'xxdl gmax kpcq zanb' #os.environ.get('EMAIL_PASS')