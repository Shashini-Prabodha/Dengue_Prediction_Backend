from flask import Flask, json, jsonify, request
from config import mongo_db

app = Flask(__name__)
app.secret_key = 'secret_key'


# routes ---------------------------------------------------------------------------------------------------------------
@app.route('/')
def root_route():
    return 'Welcome..!'


# user sign up --------------------------------------
@app.route('/sign_up', methods=["GET", "POST"])
def user_sign_up():
    user_sign_up_data = json.loads(request.data)
    print("LOG ==> ", user_sign_up_data)
    mongo_db.USER.insert_one(user_sign_up_data)
    return "User Sign Up"


# get all users  ------------------------------------
@app.route('/users', methods=["GET"])
def get_all_users():
    get_db_users = mongo_db.USER.find()
    users = []
    for data in get_db_users:
        data['_id'] = str(data['_id'])
        users.append(data)
    print(users)
    return jsonify(users)


# user update ---------------------------------------
@app.route('/user_update', methods=["PATCH"])
def user_update():
    user_updates = json.loads(request.data)
    # user_up_id = user_updates['_id']
    name = user_updates['name']
    email = user_updates['email']
    district = user_updates['district']

    mongo_db.USER.update_one({"email": email}, {"$set": {
        "name": name,
        "district": district,
    }})

    return "update user"


# user delete ---------------------------------------
@app.route('/user_delete', methods=["DELETE"])
def user_delete():
    user_deletes = json.loads(request.data)
    user_del_id = user_deletes['_id']
    mongo_db.USER.delete_one({"_id": user_del_id})
    return "User Delete"





if __name__ == '__main__':
    app.run(debug=True)
