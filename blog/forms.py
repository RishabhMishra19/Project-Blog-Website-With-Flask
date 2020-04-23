from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SelectField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from blog.model import user
from flask_wtf.file import FileField,FileAllowed





class RegistrationForm(FlaskForm):

    def validate_username(self,username):
        User=user.query.filter_by(username=username.data).first()
        if User:
            raise ValidationError('This username is already taken!! Please try different one!')

    def validate_email(self,email):
        Email=user.query.filter_by(email=email.data).first()
        if Email:
            raise ValidationError('This email is already taken!! Please try different one!')

    def validate_gender(self, gender):
        if gender.data == 'Gender':
            raise ValidationError("Please select a Gender...")

    username=StringField('username',
                         validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder":'Username'})
    email = StringField('email',
                           validators=[DataRequired(), Email()],render_kw={"placeholder":'Email'})

    gender = SelectField('gender',choices=[('Gender','Gender'),('Female','Female'),('Male','Male'),('Other','Other')])
    password = PasswordField('password',
                           validators=[DataRequired(),Length(min=8,max=20)],render_kw={"placeholder":'Password'})
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(),EqualTo('password'),
                            Length(min=8,max=20)],render_kw={"placeholder":'Confirm Password'})
    submit=SubmitField('sign-up')



class LoginForm(FlaskForm):
    email = StringField('email',
                           validators=[DataRequired(), Email()],render_kw={"placeholder":'Email'})
    password = PasswordField('password',
                           validators=[DataRequired(),Length(min=8,max=20)],render_kw={"placeholder":'Password'})
    remember=BooleanField('Remember me')
    submit=SubmitField('Login')

def edit_form_generate(current_user):
    class EditForm(FlaskForm):
        if current_user:
            nm=current_user.username
            em=current_user.email
            ge=current_user.gender

        else:
            nm = 'username'
            em = 'email'
            ge = 'gender'

        def validate_username(self,username):
            User=user.query.filter_by(username=username.data)
            if User.first():
                if User.count()==1 and User.first().username!=current_user.username:
                    raise ValidationError('This username is already taken!! Please try different one!')
                elif User.count()>1:
                    raise ValidationError('This username is already taken!! Please try different one!')


        def validate_email(self,email):
           Email=user.query.filter_by(email=email.data)
           if Email.first():
               if Email.count() == 1 and Email.first().email != current_user.email:
                   raise ValidationError('This email is already taken!! Please try different one!')
               elif Email.count() > 1:
                   raise ValidationError('This email is already taken!! Please try different one!')

        def validate_gender(self, gender):
            if gender.data == 'Gender':
                raise ValidationError("Please select a Gender...")

        username=StringField('username',
                                 validators=[DataRequired(),Length(min=2,max=20)],default=nm)
        email = StringField('email',
                                   validators=[DataRequired(), Email()],default=em)

        gender = SelectField('gender',choices=[('Gender','Gender'),('Female','Female'),('Male','Male'),('Other','Other')]
                                 ,default=ge)
        picture=FileField('profile_pic',validators=[FileAllowed(['jpg','png'])])
        submit=SubmitField('Update')
    return EditForm()


class PostForm(FlaskForm):
    title=StringField('title',validators=[DataRequired()],render_kw={"placeholder":'Title'})
    content=TextAreaField('content',validators=[DataRequired()],render_kw={"placeholder":'Content',"style":"height:150px;"})
    submit=SubmitField('Post')


def edit_postform(current_post):
    class PostForm(FlaskForm):
        if current_post:
            pt=current_post.title
            pc=current_post.content

        else:
            pt='Title'
            pc='Content'
        title = StringField('title', validators=[DataRequired()], render_kw={"placeholder": 'Title'},default=pt)
        content = TextAreaField('content', validators=[DataRequired()],
                                render_kw={"placeholder": 'Content', "style": "height:150px;"},default=pc)
        submit = SubmitField('Update')
    return PostForm()

class RequestResetForm(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email()],render_kw={"placeholder":'Email'})
    submit=SubmitField('Request Password Reset')

    def validate_email(self, email):
        Email = user.query.filter_by(email=email.data).first()
        if Email is None:
            raise ValidationError('There is no account with that email.You must register first!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password',
                             validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": 'Password'})
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password'),
                                                                     Length(min=8, max=20)],
                                     render_kw={"placeholder": 'Confirm Password'})
    submit = SubmitField('Reset Password')


class CommentForm(FlaskForm):
    comment=TextAreaField('comment',validators=[DataRequired()],render_kw={"placeholder":'Comment.....',"style":"height:150px;"})
    submit=SubmitField('Comment')




class ContactForm(FlaskForm):
    def validate_phone(self, phone):
        if not phone.data.isdigit() or len(phone.data)!=10:
            raise ValidationError('Enter a Valid Phone Number')

    name=StringField('name',
                         validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder":'Name'})
    email = StringField('email',
                           validators=[DataRequired(), Email()],render_kw={"placeholder":'Contact Email'})

    phone = StringField('phone',
                           validators=[DataRequired()],render_kw={"placeholder":'Contact Phone Number'})


    submit=SubmitField('Send')