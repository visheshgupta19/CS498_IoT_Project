"""
fish feeder 

team return to_sleep;

jj urgello
vishesh gupta
vasundhra agarwal
"""

import time
import threading
from feeder import Feeder
from fish import Fish
from service import run_server
from settings import *

def feed_schedule(fish, exit):
    while not exit.is_set():
        tm = time.strftime("%H:%M", time.localtime())
        fish.current_time = tm
    
        if (tm == FEEDTIME and fish.current_period == 0):
            fish.feed()
        elif (tm == '00:00'):
            fish.new_day()
        exit.wait(60)

def wait_for_user_terminate(fish, exit):
    while (True):
        prompt = input()
        if (prompt == 'f'): fish.feed()
        elif (prompt == 's'): fish.print_stats()
        elif (prompt == 't'): fish.new_day()
        elif (prompt == 'q'): break
        else: print("... (press 'q' to quit)")
        time.sleep(2)

    exit.set()

def begin_routine():
    feeder = Feeder()
    exit = threading.Event()
    jello = Fish(True, 0, False, feeder)

    task1 = threading.Thread(target=feed_schedule, args=(jello,exit,))
    task2 = threading.Thread(target=run_server, args=(jello,exit,))
    
    task1.start()
    task2.start()
    wait_for_user_terminate(jello, exit)

    print("cleaning...")
    feeder.cleanup()
    task1.join()
    task2.join()
    print("done")

if __name__ == "__main__":  
    print("===== FISH FEEDER ======") 
    print(" team return to_sleep;  ") 
    print(" CS 498 IoT FA2020      ") 
    print("                        ")
    print(" controls:              ")
    print(" 'f' to feed            ")
    print(" 's' for stats          ")
    print(" 't' to pass 1 day      ")
    print(" 'q' to quit            ")
    print("========================")
    begin_routine()



