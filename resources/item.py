from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()#THIS IS USED WHEN WE NEED AN  JWT ACCES TOKEN
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        #check the items in the database
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400#BAD REQUEST, item already there
        #Load the data using parser
        data = Item.parser.parse_args()
        #force = True it makes the data in json.
        item = ItemModel(name, **data)#data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500 #Internal server error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "Item Deleted"}
        return{'message': f"No item {name} found."}, 404#not found

    def put(self, name):
        data = Item.parser.parse_args()#parse the args, and put the valid ones in data, here: 'price'
        #Finding the item in the database
        item = ItemModel.find_by_name(name)
        #If it exists we updata it and it it doesnt we create it.
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)  # data['price'], data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}#List comprehension
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}#Using lambda
