from bson import json_util
from flask import Flask, json, jsonify, request, abort

from config import mongo_db

app = Flask(__name__)
app.secret_key = 'secret_key'


# routes ---------------------------------------------------------------------------------------------------------------
@app.route('/')
def root():
    return 'Welcome..!'


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    user_sign_up_data = json.loads(request.data)
    print("LOG ==> ", user_sign_up_data)
    req_user_email = user_sign_up_data['email']

    search_user_details = mongo_db.USER.find_one({"email": req_user_email})

    try:
        if search_user_details.__len__() > 0:
            return "Already exist"
    except Exception:
        print("search_user_details else ", search_user_details)

        # id = "D" + str(mongo_db.USER.count_documents({}) + 1)
        record = {
            "email": user_sign_up_data['email'],
            "name": user_sign_up_data['name'],
            "password": user_sign_up_data["password"],
            "district": user_sign_up_data['district'],
        }
        mongo_db.USER.insert_one(record)

        # mongo_db.USER.insert_one(user_sign_up_data)
        return "User Sign Up"


@app.route('/search_user', methods=["GET"])
def search_user():
    try:
        req_user_email = request.args["email"]
        print(req_user_email)
        search_user_details = mongo_db.USER.find_one({"email": req_user_email})
        # search_user_details['age']=5
        print((search_user_details))
        return json.loads(json_util.dumps(search_user_details))
    except Exception as e:
        return "null"


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
    print('email ', email)
    result = mongo_db.USER.update_one({"email": email}, {"$set": {
        "name": name,
        "district": district
    }}).raw_result.get('n')

    if result == 1:
        return "update user"
    else:
        return "null"


# user delete ---------------------------------------
@app.route('/delete_user', methods=["DELETE"])
def delete_user():
    user_deletes = json.loads(request.data)
    user_del_id = user_deletes['email']
    result = mongo_db.USER.delete_one({"email": user_del_id}).raw_result.get('n')

    if result == 1:
        return "Deleted user"
    else:
        return "null"


def renderblog():
    # filename = os.path.join(app.static_folder, 'blogs.json')
    # with open(filename) as blog_file:
    #     data = json.load(blog_file)

    with open('example.json', 'r') as myfile:
        data = myfile.read()
    # parse file
    obj = json.loads(data)

    for i in range(3):
        print("obj ", obj[i]['task'],i)
        record = {
            "_id": obj[i]['_id'],
            "task": obj[i]['task']
        }
        mongo_db.TASK.insert_one(record)

renderblog()


if __name__ == '__main__':
    app.run(debug=True)

