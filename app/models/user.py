from flask import abort
# module import
from .exceptions import AuthenticationError

class user:

    def __init__(self,username,password):
        self.username = self.checkUsername(username)
        self.password = self.checkPassword(password)


    def checkUsername(self,username):
        if username != None:
            return username
        else:
            raise AuthenticationError("Username field is incomplete or not readable")

    def checkPassword(self,password):
        if password != None:
            return password
        else:
            raise AuthenticationError("Password field is incomplete or not readable")