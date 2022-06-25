from flask import Flask, json, jsonify, request


from config import mongo_db

app = Flask(__name__)
app.secret_key = 'secret_key'


# routes ---------------------------------------------------------------------------------------------------------------
@app.route('/')
def root():
    return 'Welcome..!'

@app.route('/get_Id', methods=["GET"])
def get_Id():
    count=mongo_db.USER.count_documents({})+1
    return str(count)

# user sign up --------------------------------------
@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    user_sign_up_data = json.loads(request.data)
    print("LOG ==> ", user_sign_up_data)
    mongo_db.USER.insert_one(user_sign_up_data)
    return "User Sign Up"

@app.route('/login_user', methods=["GET"])
def search_user_login():

    req_user_email = request.args["email"]
    # print(req_user_id)
    # search_id = req_user_email['email']
    print(req_user_email)
    search_user_details = mongo_db.USER.find_one({"email": req_user_email})
    print(type(search_user_details))

    # return jsonify(search_user_details)
    return search_user_details

@app.route('/search_user', methods=["GET"])
def search_user():

    req_user_id = json.loads(request.data)
    print(req_user_id)
    search_id = req_user_id['email']
    print(search_id)
    search_user_details = mongo_db.USER.find_one({"email": search_id})
    print(type(search_user_details))

    # return jsonify(search_user_details)
    return search_user_details

# get all user  ------------------------------------
@app.route('/all_users', methods=["GET"])
def get_all_users():

    get_db_users = mongo_db.USER.find()
    users = []
    for data in get_db_users:
        data['_id'] = str(data['_id'])
        users.append(data)
    print(users)
    return jsonify(users)


# user update ---------------------------------------
@app.route('/update_user', methods=["PATCH"])
def update_user():

    user_updates = json.loads(request.data)
    name = user_updates['name']
    email = user_updates['email']
    district = user_updates['district']

    mongo_db.USER.update_one({"email": email}, {"$set": {
        "name": name,
        "district": district
    }})

    return "update user"


# user delete ---------------------------------------
@app.route('/delete_user', methods=["DELETE"])
def delete_user():
    user_deletes = json.loads(request.data)
    user_del_id = user_deletes['email']
    mongo_db.USER.delete_one({"email": user_del_id})
    return "User Delete"





if __name__ == '__main__':
    app.run(debug=True)
