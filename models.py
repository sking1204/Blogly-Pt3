from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://w7.pngwing.com/pngs/867/694/png-transparent-user-profile-default-computer-icons-network-video-recorder-avatar-cartoon-maker-blue-text-logo-thumbnail.png"


def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.Text,
                           nullable = False)
    
    last_name = db.Column(db.Text,
                          nullable = False)
    
    image_url = db.Column(db.Text,
                          nullable = False,
                          default=DEFAULT_IMAGE_URL)
    
    
    ##this will ensure all posts related to user are deleted when user is deleted:
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
  


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key = True, 
                   autoincrement = True)
    
    title = db.Column(db.Text,
                      nullable = False)
                      
    content = db.Column(db.Text,
                        nullable = False)
                      
    created_at = db.Column(db.DateTime,
                           default =datetime.now,
                            nullable = False )
                           
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                      nullable = False)
    

class Tag(db.Model):
    __tablename__="tags"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    name = db.Column(db.Text,
                     nullable = False,
                     unique = True)
    
    assignments = db.relationship('Post',secondary="posts_tags", backref="tags")
    


class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    
