# CMSC 495  - 6380   Group 6
# GROUP SIX MEMBERS: J.J. Cummings, Temiloluwa Adewale, Michael Jimoh
# DATE:              June 20, '22
# FILE:              main.py
# PURPOSE:           Create the python/flask backend for an Italian Restaurant website to complete
#                    CMSC 495's Final project
"""this runs the backend of an italian restaurant"""


from datetime import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, render_template, request


app = Flask(__name__)
app.secret_key = "JJTemiMJAdewaleJimohCummings192537293619"


# sets up a scheduler to clear stale carts every half hour
# scheduler will run in the background and will stop when the flask app is halted
cart_cleaner_scheduler = BackgroundScheduler(daemon=True)
# two triggers, every hour at 00 minutes and every hour at 30 minutes
schedule_trigger = AndTrigger([CronTrigger(hour='*', minute='00'),
                               CronTrigger(hour='*', minute='30')])
# at those intervals, run the stale cart checker
cart_cleaner_scheduler.add_job(account_management.time_checker, schedule_trigger)
cart_cleaner_scheduler.start() # begin scheduler


@app.route('/')
def home_page():
    """Displays the homepage"""
    return render_template('Homepage.html')


@app.route('/menu')
def menu_page():
    """Displays the menu page"""
    return render_template('Menu.html')


@app.route('/contact')
def socials_page():
    """Displays the social media links page"""
    return render_template('Contact.html')


@app.route('/reservation')
def reservation():
    """Displays the reservation page"""
    return render_template('Reservation.html')


@app.route('/whoops')
def error_page():
    """Displays a general error page"""
    return render_template('whoops.html')


@app.route('/login')
def sign_in_page():
    """Displays the login page"""
    return render_template('login.html')


@app.route('/signup')
def sign_up_page():
    """Displays the sign-up page"""
    return render_template('signup.html')


@app.route('/password-change')
def re_register_page():
    """Displays the account password changer page"""
    return render_template('password-editor.html')


@app.route('/cart')
def cart_page():
    """Displays the user's cart"""
    return render_template('cart-display.html')


def convert_ip(ip_str):
    """Converts an IP address into a usable string for file names"""
    fixed_ip = ip_str.replace('.', '_')
    return fixed_ip


def reconvert_ip(ip_fixed):
    """performs the reversal of convert_ip()"""
    ip_str = ip_fixed.replace('_','.')
    return original_ip


def is_logged_get():
    """Figures out if the user is logged in and returns that value"""
    if os.path.exists(cart_location):
        with open(cart_location, 'w+') as login_check:
            itemized = login_check.readLines()
            if itemized[1] == "true" or itemized[1] == "True":
                return True
            else:
                return False
    else:
        user_cart_system.create_cart(convert_ip(request.remote_addr()))
        return False


def time_checker():
    """this checks every half hour to see if user carts have gotten stale"""
    current_time = datetime.datetime.now()
    for filename in os.listdir('resources/'):
        f = os.path.join('resources/', filename)
        if os.path.isfile(f):
            with open(f) as current_file:
                lines = current_file.readlines()
                file_time = datetime.strptime(lines[2], '%m/%d/%y %H:%M:%S')
                time_delta = (current_time - file_time) / 60
                if time_delta > 30:
                    current_file.close()
                    user_cart_system.delete_cart(f)
                else:
                    current_file.close()


if __name__ == '__main__':
    app.run(debug=True)
