from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash

from . import mongo

class User (UserMixin):

    def __init__ (self, username, password, is_active = True, id = "Temp",):
        self.id = id
        self.username = username
        self.password = generate_password_hash(password, method="sha256")
        self.active = is_active

    def get_id(self):
        return self.id
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_authenticated(self):
        return self.is_active
    
    def createMongoUser(self, usersCollection):
        usersCollection.insert_one({'username': self.username, 'password': self.password})

    def removeMongoUser(self, usersCollection):
        usersCollection.find_one_and_delete({'username': self.username})