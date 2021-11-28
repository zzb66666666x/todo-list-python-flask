""" Specifies routing for the application"""
from flask import render_template, request, jsonify, make_response
from werkzeug.utils import redirect
from app import app
from app import database as db_helper

@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """
    
    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "status" in data:
            db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/", methods=['GET'])
def homepage():
    """ returns rendered homepage """
    status = {"login":False, "usr": "None"}
    user_id = request.cookies.get('userID')
    print(user_id)
    if user_id != None:
        status["usr"] = user_id
        status["login"] = True
    items = db_helper.fetch_todo()
    return render_template("index.html", items=items, status = status)

@app.route("/logout", methods=['POST'])
def logout():
    user_id = request.cookies.get('userID')
    print("current user is: ", user_id)
    status = {"login":False, "usr": "None"}
    items = db_helper.fetch_todo()
    resp = make_response(render_template("index.html", items=items, status = status))
    resp.delete_cookie(user_id)
    return resp

@app.route("/login", methods=['POST'])
def login_validate():
    requested_username = request.form['username']
    requested_password = request.form['password']
    status = {"login":False, "usr": "None"}
    items = db_helper.fetch_todo()
    # print(data)
    if requested_username == 'zzb' and requested_password == "123456":
        status["login"] = True
        status["usr"] = requested_username
        response = make_response(render_template("index.html", items = items, status = status))
        response.set_cookie('userID', requested_username)
        response.set_cookie('user_pword', requested_password)
        return response
    return render_template("index.html", items = items, status = status)