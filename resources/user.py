from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    #CHECK FOR SPECIFIC DATA NEEDED
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):
        #Add to data the specified data by the parser.
        data = UserRegister.parser.parse_args()
        #Check if user already exists
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400
        #Connect to the database and create cursor
        user = UserModel(data['username'], data['password'])#data['username'], data['password']
        user.save_to_db()

        return {"message": "User created succesfully."}, 201
