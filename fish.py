from settings import *

class Fish():
    def __init__(self, hungry, times_fed, is_dead, feeder):
        self.hungry = hungry 
        self.times_fed = times_fed # per period
        self.is_dead = is_dead
        self.feeder = feeder 

        self.current_period = 0 # in days
        self.current_time = 0 # hh:mm
        self.moved = False
        self.feeding = False
    
    def new_day(self):
        # summarize today
        self.current_period += 1
        self.is_dead = not self.moved

        # for next day
        self.moved = False
        if (self.current_period >= FEEDPERIOD):
            self.current_period = 0
            self.times_fed = 0
            self.update_hunger()

    def update_hunger(self):
        self.hungry = (self.times_fed < MAXFEED and
                not self.is_dead)

    def feed(self):
        print("FEED REQUESTED")
        self.update_hunger()
        if (self.hungry and not self.feeding):
            self.feeding = True
            self.feeder.run()
            self.times_fed += 1
            self.update_hunger()
            print("FEED DELIVERED")
            self.feeding = False
        else:
            print("FEED DENIED")

    def print_stats(self):
        print("------------------------")
        print("  FEEDTIME: " + str(FEEDTIME))
        print("  current time: " + str(self.current_time))
        print("  FEED PERIOD: " + str(FEEDPERIOD))
        print("  current period: " + str(self.current_period))
        print("  MAX FEED: " + str(MAXFEED))
        print("  times fed: " + str(self.times_fed))
        print("  hungry: " + str(self.hungry))
        print("  moved: " + str(self.moved))
        print("  is dead: " + str(self.is_dead))
        print("------------------------")

