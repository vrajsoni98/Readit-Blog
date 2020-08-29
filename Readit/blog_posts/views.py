#blog_posts/views.py
from flask import render_template,url_for,request,redirect,Blueprint
from flask_login import current_user, login_required
from Readit import db
from Readit.models import BlogPost,User
from Readit.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts',__name__)


#CREATE
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form=BlogPostForm()

    if form.validate_on_submit():
        blog_post=BlogPost(title=form.title.data,
                          text=form.text.data,
                          user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash("Your Blog has been successfuly posted",'success')
        return redirect(url_for('core.index'))
    return render_template('create_post.html',form=form,legend="New Blog Post")


#BLOG POST (VIEW) (READ)
# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post=BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',title=blog_post.title, date=blog_post.date, post=blog_post)

#DISPLAY ALL USERES
@blog_posts.route('/all_users')
@login_required
def all_users():
        users = User.query.order_by(User.username.asc())
        # blogs=BlogPost.query.filter_by(author=User.username)
        # userid = User.query.with_entities(User.id)
        # blogs = BlogPost.query(BlogPost.user_id)
        return render_template('all_users.html', users=users)


#UPDATE
@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post=BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form=BlogPostForm()

    if form.validate_on_submit():
        blog_post.title=form.title.data
        blog_post.text=form.text.data

        db.session.commit()
        flash("Post successfuly updated",'success')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))

    elif request.method=='GET':
        form.title.data=blog_post.title
        form.text.data=blog_post.text

    return render_template('create_post.html',title='Update',form=form, legend="Update Blog Post")


#DELETE
@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete(blog_post_id):
    blog_post=BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash("Post successfuly deleted",'success')
    return redirect(url_for('core.index'))
