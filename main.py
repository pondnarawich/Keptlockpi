from flask import Flask, request, render_template, redirect, flash, session, url_for, Response
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
import os
import time
import threading
import requests
import RPi.GPIO as gpio
from electromagneticlock import *
from camera import *
import json
import _thread
from read_card import *
from flask import jsonify
from flask import send_file
from subprocess import call 


template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


elec_lock = [5,6,13]
elec_lock_status = [0,1,2]
stop_threads = False
camera_slot = [0, 2, 4]
main_camera = 6

# lock1_status = 2
# lock2 = 13
# lock3 = 19
# lock4 = 26

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)
# gpio.setup(lock1, gpio.OUT)
# gpio.setup(lock2, gpio.OUT)
# gpio.setup(lock3, gpio.OUT)
# gpio.setup(lock4, gpio.OUT)
# gpio.output(lock1, True)
# gpio.output(lock2, True)
# gpio.output(lock3, True)
# gpio.output(lock4, True)
# gpio.setup(lock1_status, gpio.IN)


# led = 2
# gpio.setwarnings(False)
# gpio.cleanup()
# gpio.setmode(gpio.BCM)
# gpio.setup(led, gpio.OUT)
# gpio.output(led, False)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.session_protection = "strong"

stop_threads = False
lid = "9f45f467-8ded-4316-8229-3f0d311269ec"

# @login_manager.user_loader
# def load_user(user_id):
#     # TODO Chane to query data base kong mng either sql or no sql, this to store user info when already login

#     # mock up variable, need to be from checking with db
#     from db_struct.user import User
#     user_info = User
#     user_info.id = 12345678
#     user_info.name = "gunn"
#     user_info.username = "gnnchya"
#     user_info.email = "62011118@kmitl.ac.th"
#     user_info.password = "gnnchya"

#     return user_info


# @app.route('/keptlock/user/login')
# def login_page():
#     if current_user.is_authenticated:
#         return redirect('http://127.0.0.1:8000/keptlock/locker')
#     return render_template('login.html')


# @app.route('/keptlock/user/login', methods=['POST'])
# def login_api():
#     if current_user.is_authenticated:
#         return redirect('http://127.0.0.1:8000/keptlock/locker')
#     username = request.form['username']
#     password = request.form['password']

#     from db_struct.user import User
#     user_info_login = User(12345678, "gunn", "chai", "62011118@kmitl.ac.th", "0970047016", "gnnchya", "gnnchya", None, None, None)

#     # TODO Check the user and password in the database
#     # mock up variable, need to be from checking with db
#     user = True
#     checked_pass = True

#     # No username in the database
#     if not user:
#         flash('This username is not registered')
#         return redirect('http://127.0.0.1:8000/keptlock/user/login')
#     # wrong password
#     elif user and not checked_pass:
#         flash('Password is incorrect, Try again')
#         return redirect('http://127.0.0.1:8000/keptlock/user/login')
#     # login success
#     else:
#         login_user(user_info_login, remember=True)
#         return redirect('http://127.0.0.1:8000/keptlock/locker')


# mode_selection api
@app.route('/keptlock/mode')
# @login_required
def mode_page():
    # mock up data (UID of the locker account)
    # uid = 12345678
    # if uid != current_user.id:
    #     flash("You trying to access other's locker!")
    #     return redirect("http://127.0.0.1:8000/keptlock/locker#")

    return render_template('index.html')


@app.route('/keptlock/rfid', methods=['GET'])
# @login_required
def rfid_page():
    # mock up data (UID of the locker account)
    # uid = 12345678
    # if uid != current_user.id:
    #     flash("You trying to access other's locker!")
    #     return redirect("http://127.0.0.1:8000/keptlock/locker#")
    slots_stat = []
    for i in range(3):
        locked = is_lock(elec_lock_status[i])
        if locked == True:
            temp = False
        else:
            temp = True
        slots_stat.append(temp)

    count = 0
    for stat in slots_stat:
        if stat:
            count += 1

    open_all_allow = True
    if count == 3:
        open_all_allow = False

    return render_template('rfid.html', slots=slots_stat, open_all_allow=open_all_allow)


@app.route('/keptlock/rfid', methods=['POST', 'PUT', 'DELETE'])
# @login_required
def rfid_api():
    session.clear()
    global stop_threads
    # global stop_threads
    global rfid_slot
    stop_threads = False
    rfid_status = False

    def open_by_rfid():
        global rfid_status
        rfid_status = read_id()
        stop_threads = True
        print("RFID is already unlock")
        return
                    

    # mock up data (UID of the locker account)
    # uid = 12345678
    # if uid != current_user.id:
    #     flash("You trying to access other's locker!")
    #     return redirect("http://127.0.0.1:8000/keptlock/locker#")

    from db_struct.locker import Locker
    locker = Locker(1234, "Pitsinee", "ABCDEFG", 3, 3, 1)

    if request.method == 'POST':
        for key in request.form:
            if key.startswith('open.'):
                rfid_slot = key.partition('.')[-1]
                open_by_rfid()
                op = unlock_slot(rfid_slot)
                my_bytes_value = op.data
                my_json = my_bytes_value.decode('utf8').replace("'", '"')
                data = json.loads(my_json)
                s = json.dumps(data, indent=4, sort_keys=True)
                url = 'http://0.0.0.0:8000/keptlock/locker/update/' + str(data['lid'])
                r = requests.post(url, data=data)
                return redirect("http://127.0.0.1:5000/keptlock/rfid#")
            if key.startswith('cancel'):
                stop_threads = True
                print('Cancel na ja')
                return redirect("http://127.0.0.1:5000/keptlock/mode")
    return redirect("http://127.0.0.1:5000/keptlock/mode")


@app.route('/keptlock/pin')
# @login_required
def pin_page():
    # mock up data (UID of the locker account)
    # uid = 12345678
    # if uid != current_user.id:
    #     flash("You trying to access other's locker!")
    #     return redirect("http://127.0.0.1:8000/keptlock/locker#")

    return render_template('pin.html')


@app.route('/keptlock/pin', methods=['POST', 'PUT', 'GET', 'DELETE'])
# @login_required
def pin_api():
    # mock up data (UID of the locker account)
    # uid = 12345678
    # if uid != current_user.id:
    #     flash("You trying to access other's locker!")
    #     return redirect("http://127.0.0.1:8000/keptlock/locker#")

    if request.method == 'POST':
        pin = request.form['pin_here']

        # TODO need testing
        url = 'http://0.0.0.0:8000/keptlock/locker/unlock/validate/pin/' + lid
        code = {'code': pin}
        r = requests.get(url, data=code)
        slot = int(r.json()['slot'])
        pin_valid = False
        if r.status_code == 200:
            pin_valid = True

        if not pin_valid:
            flash("Invalid pin or expired")
            return redirect("http://127.0.0.1:5000/keptlock/pin")
        else:
            op = unlock_api(slot)
            my_bytes_value = op.data
            my_json = my_bytes_value.decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            s = json.dumps(data, indent=4, sort_keys=True)
            url = 'http://0.0.0.0:8000/keptlock/locker/update/' + str(data['lid'])
            r = requests.post(url, data=data)
            # files = {'upload_file': (str(data['vi_name'])+'avi', open(str(data['vi_path']),'rb'), 'video/avi')}
            # url = 'http://0.0.0.0:8000/keptlock/locker/video/' + str(data['lid'])
            # r = requests.post(url, files=files, data=data)

            return redirect("http://127.0.0.1:5000/keptlock/mode")

            # TODO open the slot

    return redirect("http://127.0.0.1:5000/keptlock/mode")


# hading cache and error

# for server to request the slot lock status
# @app.route('/keptlock/update/status/all')
# def update_status_api():
#     for i in 3

# input pin - update db


@app.route('/keptlock/unlock/<slot>')
def unlock_api(slot):
    response = Response()
    slot = int(slot)
    print(slot)
    global camera_recorded
    t = str(int(time.time()))
    vi_name = 'video'+t
    file_type = '.avi'
    vi_path='/home/pi/Desktop/'+vi_name+file_type
    x = threading.Thread(target=Start_record, args=(vi_path,camera_slot[slot-1],))
    x.start()
    camera_recorded = GeneralUnlock(elec_lock[slot-1], elec_lock_status[slot-1])
    Stop_record()

    data = {"lid": str(lid), "slot": str(slot), "vi_path": str(vi_path), "opened": str(False), 'vi_name': str(vi_name)}
    return jsonify(data)


def unlock_slot(slot):
    response = Response()
    slot = int(slot)
    print(slot)
    global camera_recorded
    locked = is_lock(elec_lock_status[slot-1])
    print(locked)
    if locked == True:
        t = str(int(time.time()))
        vi_name = 'video'+t
        file_type = '.avi'
        vi_path='/home/pi/Desktop/'+vi_name+file_type
        x = threading.Thread(target=Start_record, args=(vi_path,camera_slot[slot-1]))
        x.start()
        camera_recorded = GeneralUnlock(elec_lock[slot-1], elec_lock_status[slot-1])
        Stop_record()

        data = {"lid": str(lid), "slot": str(slot), "vi_path": str(vi_path), "opened": str(False), 'vi_name': str(vi_name)}

    else:
        print("locker is already unlock")
        data = "locker is already unlock"
    
    return jsonify(data)


@app.route('/keptlock/video')
def video_api():
    vi_path = request.form['vi_path']
    return send_file(vi_path,mimetype='video/avi')



@app.route('/keptlock/unlock/rfid/<slot>')
def rfid(slot):
    return read_id()
# def rfid(slot):
#     is_owner = read_id()
#     if is_owner == True:
#         op = unlock_api(slot)
#         my_bytes_value = op.data
#         my_json = my_bytes_value.decode('utf8').replace("'", '"')
#         data = json.loads(my_json)
#         s = json.dumps(data, indent=4, sort_keys=True)
#         url = 'http://0.0.0.0:8000/keptlock/locker/update/' + str(data['lid'])
#         r = requests.post(url, data=data)
#     return





@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.errorhandler(404)
def not_found(e):
    flash("Page not found")
    return render_template('error.html'), 404


@app.errorhandler(401)
def unauthorized(e):
    return redirect('http://127.0.0.1:5000/keptlock/user/login')


@app.template_filter()
def format_datetime(value, form='date'):
    if form == 'time':
        form = "HH:mm"
    elif form == 'date':
        form = "dd.MM.yy"
    return format_datetime(value, form)


if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(host='127.0.0.1', port=5000)