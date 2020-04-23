from flask import url_for,render_template,flash,redirect,request
from blog import app,db,bcrypt,mail
from blog.forms import RegistrationForm,LoginForm,edit_form_generate,PostForm,edit_postform,RequestResetForm,ResetPasswordForm,ContactForm,CommentForm
from blog.model import user , write_post,write_comment
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import  Image
from datetime import datetime
from flask_mail import Message


@app.route('/index')
@app.route('/')
def index():
    page=request.args.get('page',1,type=int)
    posts=write_post.query.order_by(write_post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('index.html',posts=posts,title='DEBUT',subtitle='A Blog Website by Rishabh Mishra')

@app.route('/register',methods=['GET','POST'])
def rform():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if  form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User=user(username=form.username.data,
                  email=form.email.data,
                  gender=form.gender.data,
                  password=hashed_password)
        db.session.add(User)
        db.session.commit()
        flash(f'Account created for {form.username.data}!!! Now login with your email and password to start!','success')
        return redirect(url_for('lform'))
    return render_template('register.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra', form=form)

@app.route('/login',methods=['GET','POST'])
def lform():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        User=user.query.filter_by(email=form.email.data).first()
        if User and bcrypt.check_password_hash(User.password,form.password.data):
            login_user(User,remember=form.remember.data)
            next_page=request.args.get('next')
            if next_page:
                next_page=next_page[1:]#to get frid of '//
            flash('Login Successful!!', 'success')
            return redirect(url_for(next_page)) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful!! Please check email and password','danger')
    return render_template('login.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra', form=form)


@app.route('/apost',methods=['GET','POST'])
def apost():
    p_id = int(request.args.get('id'))
    post_data=write_post.query.filter_by(id=p_id).first()
    post_comments=write_comment.query.order_by(write_comment.date_posted.desc()).filter_by(post_id=p_id)
    form=CommentForm()
    if form.validate_on_submit():
        if current_user.is_active:
            Comment = write_comment(comment=form.comment.data, user_id=current_user.id, post_id=p_id,
                                    post_by=current_user.username,
                                    )
            db.session.add(Comment)
            db.session.commit()
            flash(f'Commented successfully!!', 'success')
            return redirect(url_for('apost', id=p_id))

        else:
            flash('Please login for comment!', 'info')
            return redirect(url_for('lform'))


    return render_template('post.html',user=user,form=form,title='DEBUT',subtitle='A Blog Website by Rishabh Mishra',post_data=post_data,post_comments=post_comments)

@app.route('/myblog')
def myblog():
    page = request.args.get('page', 1, type=int)
    posts = write_post.query.filter_by(user_id=current_user.id).order_by(write_post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('myblog.html',posts=posts,title='DEBUT',subtitle='A Blog Website by Rishabh Mishra')

@app.route('/contact',methods=['GET','POST'])
def contact():
    form=ContactForm()
    if form.validate_on_submit():
        msg = Message('Contact Me(DEBUT)', sender='rishabhpndt19@gmail.com', recipients=[form.email.data])
        msg.body = f'''HEY {form.name.data}!
Whatsup up Buddy!
You can contact me at this Email.....'''
        mail.send(msg)
        flash('An Email is sent to the provided email Contact me through there','success')
        return redirect(url_for('contact'))
    return render_template('contact.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout Successful!!','success')
    return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
    profile_pic=url_for('static',filename='profile_image/'+current_user.image_file)
    return render_template('account.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra',profile_pic=profile_pic)

def save_picture(form_picture):
    random_text=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)#_means we wont use this var in this application
    picture_fn=random_text + f_ext
    picture_path=os.path.join(app.root_path,'static/profile_image',picture_fn)
    picture_fna = current_user.image_file
    picture_patha = os.path.join(app.root_path, 'static/profile_image', picture_fna)
    if (picture_fna)!='default.jpg':
        os.remove(picture_patha)
    output_size=(450,450)
    i=Image.open(form_picture)
    i=i.convert('RGB')
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def eform():
    form = edit_form_generate(current_user)
    profile_pic = url_for('static', filename='profile_image/' + current_user.image_file)
    if  form.validate_on_submit():
        user.query.filter_by(id=current_user.id)[0].username=form.username.data#we can also simply do current_user.username=form.username.data
        user.query.filter_by(id=current_user.id)[0].gender = form.gender.data
        user.query.filter_by(id=current_user.id)[0].email = form.email.data
        if form.picture.data:
            current_user.image_file=save_picture(form.picture.data)
        db.session.commit()
        flash(f'Profile updated successfully!!','success')
        return redirect(url_for('account'))
    return render_template('editprofile.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra', form=form,profile_pic=profile_pic)

@app.route('/create_post',methods=['GET','POST'])
@login_required
def create_post():
    form=PostForm()
    if form.validate_on_submit():
        Post = write_post(content=form.content.data,
                    title=form.title.data,
                    user_id=current_user.id)
        db.session.add(Post)
        db.session.commit()
        flash('Posted successfuly!','success')
        return redirect(url_for('myblog'))
    return render_template('create_post.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra',form=form)

@app.route('/edit_post',methods=['GET','POST'])
@login_required
def edit_post():
    p_id=int(request.args.get('id'))
    current_post=write_post.query.filter_by(id=p_id).first()
    form=edit_postform(current_post)
    if form.validate_on_submit():
        current_post.title=form.title.data
        current_post.content = form.content.data
        db.session.commit()
        flash('Updated successfuly!','success')
        return redirect(url_for('apost',id=p_id))
    return render_template('edit_post.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra',form=form)

@app.route('/delete_post',methods=['GET','POST'])
@login_required
def delete_post():
    p_id=int(request.args.get('id'))
    write_post.query.filter_by(id=p_id).delete()
    db.session.commit()
    flash('Deleted successfuly!','success')
    return redirect(url_for('myblog'))

def send_reset_email(User):
    token=User.get_reset_token()
    msg=Message('Password Reset Request(DEBUT)',sender='rishabhpndt19@gmail.com',recipients=[User.email])
    msg.body=f'''To reset your password, visit the following link:
{url_for('reset_token',token=token,_external=True)}
    
If you did not make this request then simply ignore this email and no changes wil be made. 
'''
    mail.send(msg)



@app.route("/reser_password",methods=['GET','POST'])
def reset_request():
    form=RequestResetForm()
    if form.validate_on_submit():
        User=user.query.filter_by(email=form.email.data).first()
        send_reset_email(User)
        flash('An email has been sent with instructions to reset your password to the given email','info')
        return redirect(url_for('lform'))
    return render_template('reset_request.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra',form=form)


@app.route("/reser_password/<token>",methods=['GET','POST'])
def reset_token(token):
    User=user.verify_reset_token(token)
    if User is None:
        flash('This is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form=ResetPasswordForm()
    if  form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.password=hashed_password
        db.session.commit()
        flash(f'Your Password has been updated !!! Now login with your email and password to start!','success')
        return redirect(url_for('lform'))
    return render_template('reset_token.html',title='DEBUT',subtitle='A Blog Website by Rishabh Mishra',form=form)


