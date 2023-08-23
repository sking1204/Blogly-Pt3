from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()




class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):         
        self.client = app.test_client()
        db.create_all() 

        User.query.delete()
        user= User(first_name = "Larry", last_name ="Houston") 
        db.session.add(user)    
        db.session.commit()

        self.user_id = user.id
        self.user= user
        
    

    def tearDown(self):        
       db.session.rollback()
        
    def test_list_users_route(self):
        """Checking we have a 200 -successful response from the '/users' route"""
        resp = self.client.get('/users')
        self.assertEqual(resp.status_code, 200)

   
    def test_list_users(self):
        """Checking that our new user appears in the user_list.html file render
     and that we have a OK -200 status code for the @app.route('/users')"""
        resp = self.client.get('/users')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)         
        self.assertIn('Larry Houston', html)

    def test_user_form_render(self):
        """Checking that we have all html renderd for user_form"""
        resp = self.client.get('/users/new')
        html = resp.get_data(as_text=True)
        self.assertIn('<form action="/users/new" method="POST">', html)
        self.assertIn('<input type="text" name="First Name" placeholder ="Enter a First name">', html)
        self.assertIn('<input type="text" name="Image URL" placeholder ="Provide an image of this user">', html)
        self.assertIn('<button>Add</button>', html)

####This test is failing.
##Discuss on mentor call

    def test_show_user_route(self):
    # Test an existing user
        resp = self.client.get("/4")
        self.assertEqual(resp.status_code,200)
        self.assertIn(b'User: Larry',resp.data)  





    

   
   
   
   
   
   
   
   
   
   
   