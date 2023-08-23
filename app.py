"""Blogly application."""

from flask import Flask,request,render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "aasdfjk153825"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

## Part 1

###USER ROUTES 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/')
def root():
    """Redirects to list of users"""     
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users =User.query.all()
    return render_template('users/user_list.html', users = users)

@app.route('/users/new', methods=["GET"])
def show_user_form(): 
    """Displays form to create new user"""     
    return render_template('users/user_form.html') 


@app.route('/users/new', methods = ["POST"])
def create_users():
    """Handles submission of form with new user data"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, 
                    image_url = image_url)
    db.session.add(new_user)
    db.session.commit();

    flash(f"User {new_user.first_name} {new_user.last_name} added.")

    return redirect('/users')



@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/user_detail.html", user =user)

@app.route('/users/<int:user_id>/edit')
def show_user_form_edit(user_id):     
    user = User.query.get_or_404(user_id)
    return render_template("users/user_form_edit.html", user =user)



@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    flash(f"User {user.first_name} {user.last_name} edited.")

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting existing user"""

    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.first_name} {user.last_name} deleted.")

    return redirect ("/users")

##PART 2

###POST ROUTES 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Shows new post form for user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all();
    return render_template("posts/postform.html", user=user, tags=tags) 



@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new_post_form(user_id):
    """Handles new post form submission for user"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post =Post(title=request.form['title'],
                  content=request.form['content'],
                  user=user,
                  tags=tags)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}") 






@app.route('/posts/<int:post_id>')
def show_user_post(post_id): 
    """Shows post detail"""    
    post = Post.query.get_or_404(post_id)      
    return render_template("posts/showpost.html", post =post)


@app.route('/posts/<int:post_id>/edit')
def show_post_edit(post_id): 
    """Shows post edit for for user to edit post"""    
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()      
    return render_template("posts/postformedit.html", post =post) #tags=tags


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id): 
    """Handles edit post form submission"""    
    post = Post.query.get_or_404(post_id)      
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags=Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle delete form submission"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' deleted.")
   

    return redirect(f"/users/{post.user_id}")

###TAG ROUTES 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/tags')
def list_tags():
    """Shows a list of all tags"""

    tags =Tag.query.all()
    return render_template('tags/tagslist.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Shows detail about a tag by id"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/showtag.html')

@app.route('/tags/new')
def show_new_tag_form():
   """Shows new tag form to user""" 
   posts = Post.query.all()
   return render_template('tags/newtag.html')

@app.route('/tags/new', methods =["POST"])
def post_new_tag():
    """Handles form submission for creating new tag"""

    post_ids= [int(num) for num in request.form.getlist("posts")]
    posts=Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()

    flash(f"Tag, '{new_tag.name}' added.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_form(tag_id):
    """Shows user tag edit form"""
    tag=Tag.query.get_or_404(tag_id)
    posts=Post.query.all()
    return render_template('tags/edittag.html', tag=tag, posts=posts)

@app.route ('/tags/<int:tag_id>/edit', methods=["POST"])
def post_tag_edit_form(tag_id):
    """Handles form submission for tag edit form"""
    tag=Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)

    flash(f"Tag '{tag.name} deleted.")

    return redirect ('/tags')


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)












   

   

