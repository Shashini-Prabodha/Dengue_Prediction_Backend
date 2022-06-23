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




if __name__ == '__main__':
    app.run(debug=True)
