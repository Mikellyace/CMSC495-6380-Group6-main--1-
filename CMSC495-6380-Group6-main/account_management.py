# CMSC 495  - 6380   Group 6
# GROUP SIX MEMBERS: J.J. Cummings, Temiloluwa Adewale, Michael Jimoh
# DATE:              June 20, '22
# FILE:              account_management.py
# IN SUPPORT OF:     main.py
# PURPOSE:           handle account management actions for the CMSC 495 Final Project
"""This file manipulates the user accounts for an italian restaurant"""


import re
import flask
from flask import request, redirect, flash
from passlib.hash import sha512_crypt


@app.route('/handle_data', methods=['POST', 'GET'])
def register():
    """handles the information gathered from sign_in()"""
    ip_address = flask.request.remote_addr
    registration = False
    local_logged = is_logged_get()  # keeps track of whether the user has signed in
    username = request.form['username']  # username supplied by user
    password = request.form['password']  # password supplied by user
    if request.method == 'POST':  # main info passage
        if request.form['action'] == "Log-in":  # login requested
            if local_logged is False:
                local_logged = try_login(username, password, local_logged, ip_address)
        elif request.form['action'] == "Register":  # new registration requested
            if local_logged is False:
                registration = try_register(username, password)
    if registration is True:
        return redirect("/registration_success")
    if local_logged is True:
        # log the user in
        return redirect("/success")
    # reject user login
    return redirect("/login")


def character_checker(password):
    """checks password to see if it fits all requirements to be used as a password on the site"""
    error = ""
    has_number = False
    has_lower = False
    has_upper = False
    has_special = False
    for character in password:  # checks the rest of the parameters
        if character.isdigit():  # checks for a number
            has_number = True
        if character.islower():  # checks for a lower case letter
            has_lower = True
        if character.isupper():  # checks for an upper case letter
            has_upper = True
        if re.match('[!@#$%^&*_?]', character):  # check 4 special characters
            has_special = True
    if has_number is True and has_lower is True and has_upper is True and has_special is True:
        return "True"
    else:
        if has_number is False:
            error = error + "The password must contain a number. "
        if has_lower is False:
            error = error + "The password must contain a lower case letter. "
        if has_upper is False:
            error = error + "The password must contain an upper case letter. "
        if has_special is False:
            error = error + "The password must contain an upper case letter. "
    return error


def try_login(username, password, local_logged, ip_address):
    """logs in the user"""
    with open('resources/encrypted_user_list.txt.txt', "r") as read_file:  # opens file to read
        # dissects every line in the file, separates the values and checks to see if the
        # input username is already in the file, checks the password against the encrypted
        # password in the registry
        for line in read_file:
            values = line.split()
            if values[0] == username:
                if sha512_crypt.verify(password, values[1]) is True:
                    return True
        if local_logged is False:
            error = "Username & Password Combination not found."
            flash(error)
        with open('resources/loginfailslog.txt', "w") as fail_log:
            failed = str(datetime.now()) + ", " + str(ip_address)
            fail_log.writelines(failed)
        return False


def try_register(username, password):
    """registers the user"""
    if re.match('^[0-9a-zA-Z!@#$%^&*_?]{12,}$', password):  # checks length
        if character_checker(password) == "True":  # all conditions met
            # loads file to check input against existing usernames & passwords
            with open('resources/encrypted_user_list.txt', "r") as read_file:
                exists = False
                for line in read_file:
                    values = line.split()
                    if values[0] == username:
                        exists = True
                        error = "Username already exists"
                        flash(error)
                if exists is False:  # user & pass are not in the file already
                    # open file to add to it
                    if common_pass_check(password) is False:
                        with open('resources/encrypted_user_list.txt', "a") as write_file:
                            # assemble string
                            input_to_file = "\n" + username + " " + sha512_crypt.hash(password)
                            write_file.writelines(input_to_file)  # write to file
                            return True
                    else:
                        error = "This password was found in a list of common passwords. Please " \
                                "choose a new one for you own security."
                        flash(error)
        else:
            flash(character_checker(password))
    return False


def common_pass_check(password):
    """checks the password against a table of common passwords"""
    with open('resources/common.txt', "r") as read_file:
        for line in read_file:
            if password in line:
                return True
    return False


def textfile_transfer(username, password_new):
    """transfers the contents of the passfile to the passfilebuffer minus the user who requested
    a password change then adds the new data and writes the new file back to the old location
    before deleteing itself"""
    with open('resources/encrypted_user_list.txt', 'r+') as old_file:
        with open('resources/passfilebuffer.txt', 'w+') as new_file:
            for line in old_file:  # iterate over all lines in the old file
                value2 = line.split()   # split the values of the line into username & password
                # if the value for the username is anything but the requesting user, move it to
                # the new file
                if value2[0] != username:
                    new_file.writelines(line)
            input_to_file = username + " " + sha512_crypt.hash(password_new)  # create new line
            new_file.writelines(input_to_file)  # add new line to new file
            old_file.seek(0)  # delete contents of the old file
            old_file.truncate()
    with open('resources/passfilebuffer.txt', 'r+') as buffer_file:
        with open('resources/encrypted_user_list.txt', 'w+') as final_file:
            for line in buffer_file:  # iterates over all lines in buffer file
                final_file.writelines(line)  # writes straight to original file location
            buffer_file.seek(0)  # deletes the contents of the buffer
            buffer_file.truncate()


@app.route('/reregister', methods=['POST', 'GET'])
def reregister():
    """logic for handling the changing of a password in the login system"""
    username = request.form['username']
    password_old = request.form['oldpass']
    password_new = request.form['password']
    name_found = False
    if request.method == 'POST':
        if request.form['action'] == 'Change Password':
            with open('resources/encrypted_user_list.txt', 'r') as file:
                for line in file:
                    values = line.split()
                    if values[0] == username:
                        name_found = True
                        if sha512_crypt.verify(password_old, values[1]) is True:
                            if re.match('^[0-9a-zA-Z!@#$%^&*_?]{12,}$', password_new):
                                if character_checker(password_new) == "True":
                                    if common_pass_check(password_new) is False:
                                        textfile_transfer(username, password_new)
                                        return redirect('/password-change-success')
                                    else:
                                        error = "This password was found in a list of common " \
                                                "passwords. Please choose a new one for you own " \
                                                "security."
                                        flash(error)
                                else:
                                    flash(character_checker(password_new))
                            else:
                                error = "Passwords must be more than 12 characters."
                                flash(error)
                        else:
                            error = "Your old password did not match."
                            flash(error)
                if name_found is False:
                    error = "Your username could not be found."
                    flash(error)
    return redirect("/password-change")
