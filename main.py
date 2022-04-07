from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
import os

template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    # TODO Chane to query data base kong mng either sql or no sql, this to store user info when already login

    # mock up variable, need to be from checking with db
    from db_struct.user import User
    user_info = User
    user_info.id = 12345678
    user_info.name = "gunn"
    user_info.username = "gnnchya"
    user_info.email = "62011118@kmitl.ac.th"
    user_info.password = "gnnchya"

    return user_info


@app.route('/keptlock/user/login')
def login_page():
    if current_user.is_authenticated:
        return redirect('http://127.0.0.1:8000/keptlock/locker')
    return render_template('login.html')


@app.route('/keptlock/user/login', methods=['POST'])
def login_api():
    if current_user.is_authenticated:
        return redirect('http://127.0.0.1:8000/keptlock/locker')
    username = request.form['username']
    password = request.form['password']

    from db_struct.user import User
    user_info_login = User(12345678, "gunn", "chai", "62011118@kmitl.ac.th", "0970047016", "gnnchya", "gnnchya", None, None, None)

    # TODO Check the user and password in the database
    # mock up variable, need to be from checking with db
    user = True
    checked_pass = True

    # No username in the database
    if not user:
        flash('This username is not registered')
        return redirect('http://127.0.0.1:8000/keptlock/user/login')
    # wrong password
    elif user and not checked_pass:
        flash('Password is incorrect, Try again')
        return redirect('http://127.0.0.1:8000/keptlock/user/login')
    # login success
    else:
        login_user(user_info_login, remember=True)
        return redirect('http://127.0.0.1:8000/keptlock/locker')


# mode_selection api
@app.route('/keptlock/mode')
@login_required
def mode_page():
    # mock up data (UID of the locker account)
    uid = 12345678
    if uid != current_user.id:
        flash("You trying to access other's locker!")
        return redirect("http://127.0.0.1:8000/keptlock/locker#")

    return render_template('index.html')


@app.route('/keptlock/rfid')
@login_required
def rfid_page():
    # mock up data (UID of the locker account)
    uid = 12345678
    if uid != current_user.id:
        flash("You trying to access other's locker!")
        return redirect("http://127.0.0.1:8000/keptlock/locker#")

    from db_struct.locker import Locker
    locker = Locker(1234, "Pitsinee", "ABCDEFG", 3, 3, 1)

    from db_struct.slot import Slot
    slot1 = Slot(1, False)
    slot2 = Slot(1, False)
    slot3 = Slot(1, True)

    slots = [slot1, slot2, slot3]

    return render_template('rfid.html', locker=locker, slots=slots)


@app.route('/keptlock/rfid', methods=['POST', 'PUT', 'GET', 'DELETE'])
@login_required
def rfid_api():
    # mock up data (UID of the locker account)
    uid = 12345678
    if uid != current_user.id:
        flash("You trying to access other's locker!")
        return redirect("http://127.0.0.1:8000/keptlock/locker#")

    from db_struct.locker import Locker
    locker = Locker(1234, "Pitsinee", "ABCDEFG", 3, 3, 1)

    if request.method == 'POST':
        for key in request.form:
            if key.startswith('open.'):
                slot = key.partition('.')[-1]
                if slot == locker.size + 1:
                    # TODO do something with the locker
                    print("open all slots")
                else:
                    # TODO do something with the locker
                    print("turn on slot no.", slot)

    return redirect("http://127.0.0.1:8000/keptlock/rfid")


@app.route('/keptlock/pin')
@login_required
def pin_page():
    # mock up data (UID of the locker account)
    uid = 12345678
    if uid != current_user.id:
        flash("You trying to access other's locker!")
        return redirect("http://127.0.0.1:8000/keptlock/locker#")

    return render_template('pin.html')


@app.route('/keptlock/pin', methods=['POST', 'PUT', 'GET', 'DELETE'])
@login_required
def pin_api():
    # mock up data (UID of the locker account)
    uid = 12345678
    if uid != current_user.id:
        flash("You trying to access other's locker!")
        return redirect("http://127.0.0.1:8000/keptlock/locker#")

    if request.method == 'POST':
        pin = request.form['pin_enter']
        # TODO check pin in the database and get slot no.
        slot = 1
        pin_exist = False
        pin_expired = False
        if not pin_exist:
            flash("Invalid pin")
            return redirect("http://127.0.0.1:8000/keptlock/pin")
        elif pin_expired:
            flash("Pin expired")
            return redirect("http://127.0.0.1:8000/keptlock/pin")
        else:
            print(pin, "open slot no.", slot)
            # TODO open the slot

    return redirect("http://127.0.0.1:8000/keptlock/mode")


# hading cache and error

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
    return redirect('http://127.0.0.1:8000/keptlock/user/login')


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
    app.run(host='127.0.0.1', port=8000)