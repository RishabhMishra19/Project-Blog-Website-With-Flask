from blog import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as serializer
from blog import app
@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


class user(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), unique=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,default='default.jpg')
    password=db.Column(db.String(20),nullable=False)
    posts=db.relationship('write_post',backref='author',lazy=True)#backref allowed us to access post columns
    def get_reset_token(self):
        s=serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id})
    @staticmethod#telling python that not to expect self parameter here
    def verify_reset_token(token, max_age = 1800):
        s=serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token, max_age)['user_id']
        except:
            return None
        return user.query.get(user_id)

    def __repr__(self):
        return f"user('{self.username}','{self.email}','{self.image_file}','{self.gender}')"

class write_post(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)#i am not paasing current time i am passing func thats why () are not used
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comments = db.relationship('write_comment', backref='author_post', lazy=True)  # backref allowed us to access post columns

    def __repr__(self):
        return f"post('{self.id}','{self.title}','{self.date_posted}','{self.user_id}')"


class write_comment(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)#i am not paasing current time i am passing func thats why () are not used
    comment=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('write_post.id'),nullable=False)
    post_by = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"post('{self.id}','{self.comment}','{self.date_posted}','{self.user_id}','{self.post_by_img_file}','{self.post_id}','{self.post_by}')"

