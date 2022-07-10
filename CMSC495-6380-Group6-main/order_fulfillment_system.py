# CMSC 495  - 6380   Group 6
# GROUP SIX MEMBERS: J.J. Cummings, Temiloluwa Adewale, Michael Jimoh
# DATE:              June 30, '22
# FILE:              order_fulfillment_system.py
# IN SUPPORT OF:     main.py
# PURPOSE:           simulates the kitchen ordering system for the CMSC 495 Final Project
"""This file pretends to be an order fulfillment system in an italian restaurant's kitchen"""


# imports!
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


# everything from this comment to the completion of maintain_timer pertains to maintaining a count
# of minutes until all orders in the OFS are complete.
# This block sets up a timer which runs in the background and is deleted when the program stops
order_scheduler = BackgroundScheduler(daemon=True)
# the scheduler will check every minute
schedule_trigger = CronTrigger(minute='*')
# the schedules will run maintain_timer on the schdule above
order_scheduler.add_job(maintain_timer, schedule_trigger)
# the schduler begins
order_scheduler.start()


# this variable tracks how many minutes are left until all order in the OFS should be complete
global_order_time = []  # placing global variables in arrays allows them to be mutable and stops
# python from throwing errors
global_order_time[0] = 0  # this is the only variable we'll use, it counts the number of minutes
# until all orders are cleared from the order board


def maintain_timer():
    """This method reduces the total estimated completion time of all orders by 1"""
    local_order_time = global_order_time[0]  # pull class variable
    if local_order_time >= 1:  # if the time is greater than or equal to one minute, decriment
        local_order_time = local_order_time - 1
    elif local_order_time <= 0:  # if there are no more orders in completion or if the clock somehow
        # ran into the negative, set the time to 0
        local_order_time = 0
    global_order_time[0] = local_order_time  # push the altered time back to the class variable


def ordering(order):
    """This adds each order to the times and returns the total time to completion for the order"""
    total_order_time = 0  # this counts the amount of time an argument order should take
    with open("o_f_s_resources/ETA_times.txt", 'r') as times:  # open the ETA times file
        for item in order:  # for every line in the order
            item_line = item.split()  # break the line down into an array stating what the ordered
            # item is, and how many were ordered. There will be additional information
            # after this, but it is irrelevant to this process
            eta_itemized = times.readlines()  # split the ETA times file into each line
            for line in eta_itemized:  # for every line in the ETA file
                line_itemized = line.split()  # break the line into the menu item and the ETA
                if item_line[0] == line_itemized[0]:  # if the ETA file line contains the suspect
                    # order item:
                    total_order_time = total_order_time + (item[1] * line_itemized[1])  # multiply
                    # the number of those items by the completion time for each one and add it to
                    # the estimated completion time for the order
    times.close()
    return global_order_time[0]
