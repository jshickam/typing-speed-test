import queue
from re import S
from tkinter import Canvas, Frame, Label
import time
from threading import Thread
from queue import Queue

from sqlalchemy import false

class Timer(Frame):
    def __init__(self, parent, callback, initial_time=0):
        """Parent is a tkinter object, initial time is seconds as an integer value"""
        super().__init__(parent)
        self.time_label = Label(self, text=self.format_time(initial_time), font=("Menlo", 40))
        self.time_label.grid(column=0, row=0)
        self.window = parent
        self.callback = callback
        self.paused = False
        self.paused_time = 0

    def start(self, seconds=0):
        """Starts the countdown in a new thread to prevent blocking
        seconds is the time in seconds to run the timer"""
        # create a Queue object to store the timer status
        queue = Queue()
        # start the thread
        self.countdown_thread = Thread(target=self.countdown, args=(seconds, queue, ), daemon=True)
        self.countdown_thread.start() 
    
    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        tm = self.paused_time
        self.paused_time = 0
        self.start(tm)

    def countdown(self, seconds, queue):
        """Counts down from the supplied number of seconds and updates the timer label using
        Queue object (queue)"""
        while seconds > -1 and not self.paused:
            queue.put(seconds)
            self._update_time(queue)
            time.sleep(1)
            seconds -= 1
        self.paused_time = seconds

    def _update_time(self, queue):
        """Updates the timer label using the Queue object (queue)"""
        seconds = queue.get(block=False)
        self.time_label.configure(text=self.format_time(seconds))
        self.window.update()
        if seconds == 0:
            self.callback()

    @staticmethod
    def format_time(seconds):
        #Format minutes and seconds to 2 characters
        minutes_string = "{:02d}".format(int(seconds / 60))
        seconds_string = "{:02d}".format(seconds % 60)
        return f"{minutes_string}:{seconds_string}"