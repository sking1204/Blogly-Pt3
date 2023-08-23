from models import User,Post,Tag,PostTag, db
from app import app

#Create all tables
db.drop_all()
db.create_all()

#If table isn't empty, empty it
User.query.delete()

#Add users
john = User(first_name='John', last_name ='Smith')
karen = User(first_name='Karen', last_name ='Spring')
sally = User(first_name='Sally', last_name ='Adams')
muffin = User(first_name= 'Muffin', last_name ='Cat', image_url ='https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80')


#Add new objects to session, so they'll persist
db.session.add(john)
db.session.add(karen)
db.session.add(sally)
db.session.add(muffin)

#Commit -- otherwise, this never gets saved!
db.session.commit()

####images
##https://w7.pngwing.com/pngs/6/315/png-transparent-harry-potter-and-the-deathly-hallows-harry-potter-and-the-goblet-of-fire-lord-voldemort-harry-potter-thumbnail.png

##https://w7.pngwing.com/pngs/175/716/png-transparent-harry-potter-and-the-philosopher-s-stone-hermione-granger-harry-potter-thumbnail.png

##https://w7.pngwing.com/pngs/413/670/png-transparent-hogwarts-gryffindor-house-harry-potter-harry-potter-emblem-logo-infant-thumbnail.png

##https://w7.pngwing.com/pngs/758/684/png-transparent-brown-owl-with-brown-envelope-harry-potter-and-the-philosopher-s-stone-owl-hedwig-hogwarts-harry-potter-fauna-bird-feather-thumbnail.png
