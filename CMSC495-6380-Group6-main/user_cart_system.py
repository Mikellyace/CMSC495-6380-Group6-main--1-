# CMSC 495  - 6380   Group 6
# GROUP SIX MEMBERS: J.J. Cummings, Temiloluwa Adewale, Michael Jimoh
# DATE:              June 30, '22
# FILE:              user_cart_system.py
# IN SUPPORT OF:     main.py
# PURPOSE:           handle file operations on cart files for the CMSC 495 Final Project
"""This file manipulates the user cart files for an italian restaurant"""


from datetime import datetime
import os
from flask import redirect


def create_cart(ip_):
    """creates user carts for designated ip address"""
    cart_location ='carts/' + ip_ + '.txt'
    with open(cart_location, 'a') as new_cart:
        new_cart.write(ip_+"\n")
        new_cart.write("false")
        now = datetime.datetime.now()
        new_cart.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        new_cart.write("\n")
        new_cart.close()


def new_time(ip_):
    """edits cart files with the time at which they were last evaluated to be edited"""
    cart_location = 'carts/' + ip_ + '.txt'
    try:
        if os.path.exists(cart_location):
            with open(cart_location, 'w+') as cart:
                itemized = cart.readLines()
                now = datetime.datetime.now()
                itemized[2] = now.strftime("%Y-%m-%d %H:%M:%S")
                cart.writelines(itemized)
        else:
            create_cart(ip_)
    except FileNotFoundError:
        create_cart(ip_)

def add_item(ip_, new_item):
    """adds a new item to the requested cart"""
    cart_location = 'carts/' + ip_ + '.txt'
    try:
        if os.path.exists(cart_location):
            with open(cart_location, 'w+') as cart:
                itemized = cart.readLines()
                now = datetime.datetime.now()
                itemized[2] = now.strftime("%Y-%m-%d %H:%M:%S")
                cart.writelines(itemized)
                cart.write(new_item)
                cart.close()
        else:
            create_cart(ip_)
            with open(cart_location, 'w+') as cart:
                cart.write(new_item)
                cart.close()
        return None
    except:
        return redirect("/whoops")


def edit_item(ip_, line, edit):
    """edits an item from the requested cart at the given line"""
    cart_location = 'carts/' + ip_ + '.txt'
    try:
        if os.path.exists(cart_location):
            with open(cart_location, 'w+') as cart:
                itemized = cart.readLines()
                now = datetime.datetime.now()
                itemized[2] = now.strftime("%Y-%m-%d %H:%M:%S")
                itemized[line] = edit
                cart.writelines(itemized)
                cart.close()
        else:
            create_cart(ip_)
            add_item(ip_, edit)
        return redirect("/cart")
    except:
        return redirect("/whoops")


def delete_item(ip_, line):
    """deletes an item from the requested cart at the given line"""
    cart_location = 'carts/' + ip_ + '.txt'
    try:
        if os.path.exists(cart_location):
            with open(cart_location, 'w+') as cart:
                itemized = cart.readLines()
                now = datetime.datetime.now()
                itemized[2] = now.strftime("%Y-%m-%d %H:%M:%S")
                itemized.delete(line)
                cart.writelines(itemized)
                cart.close()
        else:
            create_cart(ip_)
        return redirect("/cart")
    except:
        return redirect("/whoops")


def delete_cart(cart_location):
    """deletes a user's entire cart"""
    if os.path.exists(cart_location):
        os.remove(cart_location)
    return redirect("/")


def sign_in(ip_):
    """marks the cart file of a given user to denote that the user is logged in"""
    cart_location = 'carts/' + ip_ + '.txt'
    try:
        if os.path.exists(cart_location):
            with open(cart_location, 'w+') as cart:
                itemized = cart.readlines()
                itemized[1] = "true"
                now = datetime.datetime.now()
                itemized[2] = now.strftime("%Y-%m-%d %H:%M:%S")
                cart.writelines(itemized)
                cart.close()
        else:
            create_cart(ip_)
            with open(cart_location, 'w+') as cart:
                itemized = cart.readlines()
                itemized[1] = "true"
                cart.writelines(itemized)
                cart.close()
        return None
    except:
        return redirect("/whoops")
