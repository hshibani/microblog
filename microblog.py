# Instance of the application -app ( an instance variable)
# Package name - app
# from package-app import the microblog application instance-app
from app import app, db
from app.models import User, Post

# app.shell_context_processor is a decorator which registers the function as a shell context function
@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User' : User, 'Post' : Post}