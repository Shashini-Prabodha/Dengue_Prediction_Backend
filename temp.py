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


@app.route('/user')
def user():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("select avg(value) as pred from dengue_d.dd where date like '%01-01' and city='colombo'")
        rows = cur.fetchall()
        res = jsonify(rows)
        res.status = 200
        return res
    except Exception as e:
        print(e)


@app.route('/userss/<city>')
def disctric(city):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        # cur.execute("""select avg(Value) as pred from dengue_d.dd where Date like '%01-01' and City = %s""", (city))
        # # rows = cur.fetchall()
        # # res = jsonify(rows)
        # r = [dict((cur.description[i][0], value)
        #           for i, value in enumerate(row)) for row in cur.fetchall()]
        # return 'working this method'

        print(city)

        # query2 = ("Select * from dengue_d.dd where Date like '%01-01' and city=' " + city + "'")
        # # query2 = ("select avg(value) as pred from dengue_d.dd where date like '%01-01' and city='colombo'")
        # myresult2 = cur.execute(query2)
        # # print(myresult2)
        # return jsonify(myresult2)
        # rows = cur.fetchall()
        # res = jsonify(rows)
        # res.status = 200
        # return res

        # conn = mysql.connect()
        # cursor = conn.cursor(pymysql.cursors.DictCursor)
        likeString = "'%%" + '01-01' + "'"
        # cursor.execute("select avg(Value) as pred from dengue_d.dd where Date like %s and City = %s, (likeString,city))
        # row = cursor.fetchone()
        # resp = jsonify(row)
        # resp.status_code = 200
        # return row

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select avg(value) from dengue_d.dd where city = %s and  date like '%%01-01' ", (city))
        rows = cursor.fetchall()
        print(rows)
        return jsonify(rows)


    except Exception as e:
        print(e)
        return e


# @app.route('/search/<param1>/<param2>/<param3>')
# def get(param1, param2, param3):
#     cur = mysql.connect().cursor()
#     cur.execute('''select * from maindb.maintable where field1 = %s and field2 = %s and field3 = %s''',
#                 (param1, param2, param3))
#     r = [dict((cur.description[i][0], value)
#          for i, value in enumerate(row)) for row in cur.fetchall()]
#     return jsonify({'results': r})

if __name__ == "__main__":
    app.run(debug=True)


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