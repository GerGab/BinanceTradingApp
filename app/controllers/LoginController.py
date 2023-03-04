# dependencies import
from flask_jwt_extended import create_access_token
import logging
# modules import
from ..models.user import user
from ..models.exceptions import AuthenticationError
from config import adminUser

log = logging.getLogger('app.auth')

def login(username,password):

    User = user(username,password)
    if User.username == adminUser.ADMIN and User.password == adminUser.PASSWORD:
        jwt = create_access_token(identity=User.username)
        log.info('Admin access granted')
        return jwt
    else:
        log.warning('unauthorized atempt to login')
        raise AuthenticationError("Login error, password or username no correct")