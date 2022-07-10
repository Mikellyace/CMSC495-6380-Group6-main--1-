# CMSC 495  - 6380   Group 6
# GROUP SIX MEMBERS: J.J. Cummings, Temiloluwa Adewale, Michael Jimoh
# DATE:              June 30, '22
# FILE:              point_of_sale_system.py
# IN SUPPORT OF:     main.py
# PURPOSE:           simulates the 3rd party POS system for the CMSC 495 Final Project
"""This file pretends to be a 3rd party POS system for an italian restaurant"""
"""This is *NOT* intended to function as an actual POS, only a facsimile for a third party POS"""


def take_payment(first, middle, last, address1, address2, city, state, zip, cardno, cvv):
    """take in payment information and return a true or false value for the payment status"""
    if first & last & address1 & city & state & zip & cardno & cvv:
        return True
    else:
        return False
