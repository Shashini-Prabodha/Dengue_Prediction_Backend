from bson import json_util
from flask import Flask, json, jsonify, request, session

from config import mongo_db
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1023'
app.config['MYSQL_DATABASE_DB'] = 'dengue_d'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

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

        session['email']=user_sign_up_data['email']
        session["name"] = user_sign_up_data['name']
        session["password"] = user_sign_up_data["password"]
        session["district"] = user_sign_up_data['district']

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

        print(e)
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

@app.route('/login_user', methods=["GET"])
def search_user_login():

    req_user_email = request.args["email"]
    # print(req_user_id)
    # search_id = req_user_email['email']
    print(req_user_email)
    search_user_details = mongo_db.USER.find_one({"email": req_user_email})
    print(type(search_user_details))
    return jsonify(search_user_details)
    # return search_user_details

    # return jsonify(search_user_details)
    return search_user_details


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


# get zone
# @app.route('/getzone', methods=["GET"])
def getPredict(city):
    print('in')
    # city =json.loads(request.data)
    # print(city['city'])
    try:
        # req_user_email = request.json
        # print(req_user_email)
        conn = mysql.connect()
        print("1")
        cursor = conn.cursor()
        cursor.execute("select avg(value) from dengue_d.dd where city = %s and  date like '%%01-01' ",city)
        print("2")
        rows = cursor.fetchall().__getitem__(0)
        print(rows)
        list=[]
        for data in rows:
            list.append(float(data))

        predict=int(round(list[0]))
        session['this_month_pred']=predict

        if predict >= 800:
            session['zone'] = "Red"
        elif predict >=200:
            session['zone'] = "Yellow"
        else:
            session['zone'] = "Green"

        return predict

    except Exception as e:
        print(e)
        return e


# save task list on start
def renderblog():
    # filename = os.path.join(app.static_folder, 'blogs.json')
    # with open(filename) as blog_file:
    #     data = json.load(blog_file)

    with open('example.json', 'r') as myfile:
        data = myfile.read()
    # parse file
    obj = json.loads(data)
    count = mongo_db.TASK.count_documents({})
    print("count ", count)
    if count <= 0:
        for i in range(10):
            print("obj ", obj[i]['task'], i)
            record = {
                "_id": obj[i]['_id'],
                "task": obj[i]['task']
            }
            mongo_db.TASK.insert_one(record)


renderblog()

if __name__ == '__main__':
    app.run(debug=True)
