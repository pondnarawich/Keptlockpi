from flask import Flask, request, render_template, redirect, flash, session, url_for
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


template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


elec_lock = [5,6,13]
elec_lock_status = [0,1,2]


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
lid = "95299d5b-5b9f-49fc-b8d9-f2b7e96190ba"

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


@app.route('/keptlock/rfid')
# @login_required
def rfid_page():
    # mock up data (UID of the locker account)
    # uid = 12345678
    # if uid != current_user.id:
    #     flash("You trying to access other's locker!")
    #     return redirect("http://127.0.0.1:8000/keptlock/locker#")
    slots = []

    count = 0
    for slot in slots:
        if slot.opened:
            count += 1

    open_all_allow = True
    if count == 3:
        open_all_allow = False

    return render_template('rfid.html', slots=slots, open_all_allow=open_all_allow)


@app.route('/keptlock/rfid', methods=['POST', 'PUT', 'GET', 'DELETE'])
# @login_required
def rfid_api():
    global stop_threads

    def open_locker(slot_no):
        url = "http://127.0.0.1:8000/keptlock/locker/unlock/" + lid;
        timeout = time.time() + 60  # 1 minute
        done = False
        if slot == "all":
            print("open all")
            status = [True, True, True]
            while True:
                # TODO do something with the locker
                print("open all")
                # If RFID is authen then done = True
                if stop_threads or time.time() > timeout or done:
                    if done:
                        r = requests.post(url, data=status)
                        print(r.status_code, r.reason, r.content)
                        url_vid = "http://127.0.0.1:8000/keptlock/locker/video"

                        for i in range(3):
                            files = {'vid1': open('PATHHHHHHHHHHH', 'rb'), 'vid2': open('PATHHHHHHHHHHH', 'rb')}
                            data = {"lid": lid, "slot": i}
                            r = requests.post(url_vid, data=data, files=files)
                            print(r.status_code, r.reason, r.content)

                        break
        else:
            print("open slot#", slot_no)
            status_now = [False, False, False]
            status_now[slot_no-1] = True
            status = {"slots": status_now}
            while True:
                # TODO do something with the locker
                print("open slot#", slot_no)
                # If RFID is authen then done = True
                if stop_threads or time.time() > timeout or done:
                    if done:
                        r = requests.post(url, data=status)
                        print(r.status_code, r.reason, r.content)

                        url_vid = "http://127.0.0.1:8000/keptlock/locker/video"
                        files = {'vid1': open('PATHHHHHHHHHHH22', 'rb'), 'vid2': open('PATHHHHHHHHHHH', 'rb')}
                        data = {"lid": lid, "slot": slot_no}
                        r = requests.post(url_vid, data=data, files=files)
                        print(r.status_code, r.reason, r.content)
                        break

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
                slot = key.partition('.')[-1]
                if slot == "all":
                    print("open all slots")
                    x = threading.Thread(target=open_locker, args=("all",))
                    x.start()
                    return redirect("http://127.0.0.1:5000/keptlock/rfid#popup"+ str(locker.size + 1))
                else:
                    print("turn on slot no.", slot)
                    x = threading.Thread(target=open_locker, args=(slot,))
                    x.start()
                    return redirect("http://127.0.0.1:5000/keptlock/rfid#popup"+slot)
            if key.startswith('cancel'):
                stop_threads = True
                return redirect("http://127.0.0.1:5000/keptlock/rfid#")
    return redirect("http://127.0.0.1:5000/keptlock/rfid#")


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
        pin = request.form['pin_enter']

        # TODO need testing
        url = "http://127.0.0.1:5000/keptlock/locker/unlock/pin" + lid;
        code = {'code': pin}
        r = requests.post(url, data=code)
        print(r.status_code, r.reason, r.content)

        slot = int(r.content)
        pin_valid = False
        if r.status_code == 200:
            pin_valid = True

        if not pin_valid:
            flash("Invalid pin or expired")
            return redirect("http://127.0.0.1:5000/keptlock/pin")
        else:
            url = "http://127.0.0.1:8000/keptlock/locker/unlock/" + lid;
            print(pin, "open slot no.", slot)
            status_now = [False, False, False]
            status_now[slot - 1] = True
            status = {"slots": status_now}

            r = requests.post(url, data=status)
            print(r.status_code, r.reason, r.content)

            # TODO open the slot

    return redirect("http://127.0.0.1:5000/keptlock/mode")


# hading cache and error

@app.route('/keptlock/unlock/<slot>')
def unlock_api(slot):
    slot = int(slot)
    print(slot)
    global camera_recorded
    locked = is_lock(elec_lock_status[slot-1])
    print(locked)
    if locked == True:
        tm = time.time()
        t = str(tm)
        vi_path='/home/pi/Desktop/video'+t+'.avi'
        x = threading.Thread(target=Start_record, args=(vi_path,))
        x.start()
        camera_recorded = GeneralUnlock(elec_lock[slot-1], elec_lock_status[slot-1])
        Stop_record()
        
        url_vid = "http://127.0.0.1:8000/keptlock/locker/video"
        files = [('vid1', (vi_path, open(vi_path, 'rb'), 'video/avi')) , ('vid2', (vi_path, open(vi_path, 'rb'), 'video/avi'))]
        data = {"lid": lid, "slot": slot}
        r = requests.post(url_vid, data=data, files=files)
        print(r.status_code, r.reason, r.content)
    else:
        print("locker is already unlock")

    status = is_lock(elec_lock_status[slot-1])
    if status == True:
        status = False
    else:
        status=True
    print(status)
    return jsonify(status)


@app.route('/keptlock/unlock/rfid/<slot>')
def rfid(slot):
    is_owner = read_id()
    if is_owner == True:
        slot = int(slot)
        global camera_recorded
        locked = is_lock(elec_lock_status[slot-1])
        print(locked)
        if locked == True:
            _thread.start_new_thread(Start_record,())
            camera_recorded = GeneralUnlock(elec_lock[slot-1], elec_lock_status[slot-1])
            Stop_record()
            json_string = '''
            {
            "response": "locker rfid unlock"
            } '''
        else:
            print("locker is already unlock")
            json_string = '''
            {
            "response": "locker is already unlock"
            } '''
    else:
        print("u are not the owner")
        json_string = '''
            {
            "response": "u are not the owner"
            } '''

    
    return json.loads(json_string)





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