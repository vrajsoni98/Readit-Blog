
from flask import render_template,url_for,redirect,flash,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from Readit import db
from Readit.models import User,BlogPost
from Readit.users.forms import RegistrationForm,LoginForm,UpdateUserForm

from Readit.users.picture_handler import add_profile_pic


users=Blueprint('users',__name__)

#Registration
@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash(f'{current_user.username} already logged in','warning ')
        return redirect(url_for('core.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)



@users.route('/login',methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        flash(f'{current_user.username} already logged in','warning ')
        return redirect(url_for('core.index'))
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        #.first() is used so that we do not get user in list format

        if user is None:
            flash('Invalid!! Please check your Email and Password','danger')

        elif user.check_password(form.password.data) and user is not None:
            login_user(user,remember=form.remember.data)
            flash('Login Successful','success')

            next=request.args.get('next')

            if next == None or not next[0]=='/':
                next=url_for('users.account')

            return redirect(next)
        else:
            flash('Invalid!! Please check your Email and Password','danger')
    return render_template('login.html',form=form)



#LogOut
@users.route("/logout")
def logout():
    flash(f'{current_user.username} logged out','success ')
    logout_user()
    return redirect(url_for('core.index'))


#Account
@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form=UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username=current_user.username
            pic=add_profile_pic(form.picture.data,username)
            current_user.profile_image=pic

        current_user.username=form.username.data
        current_user.email=form.email.data

        db.session.commit()
        flash(f'{current_user.username} Account Updated!','success')
        return redirect(url_for('users.account'))

    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email

    profile_image=url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)


#user's list of BlogPost

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=3)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
