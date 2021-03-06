from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    user =  UserModel.find_by_username(username)# We look athe database now instead of list up here
    if user and safe_str_cmp(user.password, password):# string compare even if the encoding is different.
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

