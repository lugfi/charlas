import flask
import psycopg2

app = flask.Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello world'

@app.route('/echo/<message>')
def echo_service(message):
    return message

@app.route('/user/<name>', methods = ['GET', 'POST'])
def user_service(name):
    host = "pg-server"
    params = "user='postgres' dbname='test' host='{}' password='qwerty'".format(host)
    response = ""
    if flask.request.method == 'GET':
        try:
            print("Connecting with: ", params)
            conn = psycopg2.connect(params)
            cur = conn.cursor()
            cur.execute("select * from test_table where (name = %s)", [name])
            rows = cur.fetchall()
            response = "Registers found: {}".format(len(rows))
            cur.close()
            conn.close()
            for row in rows:
                response += "User:{} Food: {}\n".format(row[0], row[1])
        except Exception as e:
            print str(e)
    if flask.request.method == 'POST':
        food = flask.request.get_data()
        print "inserting('{}', '{}')".format(name, food)
        try:
            print("Connecting with: ", params)
            conn = psycopg2.connect(params)
            cur = conn.cursor()
            cur.execute("insert into test_table values (%s, %s)", [name, food])
            conn.commit()
            cur.close()
            conn.close
        except Exception as e:
            print str(e)
    return response

@app.route('/users')
def all_users_service():
    host = "pg-server"
    params = "user='postgres' dbname='test' host='{}' password='qwerty'".format(host)
    response = ""
    try:
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute("select * from test_table")
        rows = cur.fetchall()
        response = "Registers found: {}\n".format(len(rows))
        cur.close()
        conn.close()
        for row in rows:
            response += "User:{} Food: {}\n".format(row[0], row[1])
    except Exception as e:
        print str(e)
    return response

def main():
    app.run(host="0.0.0.0")

if __name__ == '__main__':
    main()
