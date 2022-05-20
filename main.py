from tkinter import Button, Entry, Tk, Text as txt, messagebox, END
import tkinter as tk
from typing import Text

from matplotlib.pyplot import text
from timer import Timer
from text_entry import TextEntry
from generator import SentenceGenerator

TEST_LENGTH = 30  #Test length in seconds
NUMBER_OF_SENTENCES = 30

global sentences

def count_down_end():
    # Start text when countdown ends
    timer.callback = end_test
    
    #Set up test
    reading_area.configure(state="normal")
    reading_area.delete('1.0', END)
    typing_area.delete('1.0', END)
    global sentences
    reading_area.insert(1.0, sentences)
    typing_area.set_test_text(sentences=sentences)
    typing_area.configure(state="normal")
    typing_area.focus()
    timer.start(TEST_LENGTH)
    start_button.configure(text="Pause")

def end_test():
    # Display test results
    words, errors = typing_area.get_score()
    wpm = words / (TEST_LENGTH / 60)
    accuracy = 100 - 100 * (errors / words)
    message_string = f"Time: {TEST_LENGTH} seconds\nTotal Words: {words}\nErrors: {errors}\nWords Per minute: {wpm}\nAccuracy: {accuracy}"
    messagebox.showinfo(title="Test Results", message=message_string, )
    timer.callback = count_down_end
    start_button.configure(text="Start")

def start_button_click():
    # Get random sentences
    sentence_generator = SentenceGenerator()
    global sentences
    sentences = sentence_generator.get_random(NUMBER_OF_SENTENCES)

    if start_button.cget("text") == "Start":
        timer.start(3)
        start_button.configure(text="Get Ready")
    elif start_button.cget("text") == "Pause":
        timer.pause()
        start_button.configure(text="Resume")
    elif start_button.cget("text") == "Resume":
        timer.resume()
        start_button.configure(text="Pause")


window = Tk()
window.geometry("810x725")
window.title("Typing Test")
window.resizable(False, False)
window.configure(padx=5)
timer = Timer(window, callback=count_down_end, initial_time=0)
timer.grid(column=0, row=0, padx=(98,0))

#start countdown
start_button = Button(window, text="Start", command=start_button_click, width=6) 
start_button.grid(column=2, row=0)


#Create Text object to display test
reading_area = txt(window) #, sentences)
reading_area.configure(wrap="word", state="disable")
reading_area.grid(column=0, row=2, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)

# Set up typing area
typing_area = TextEntry(window)
typing_area.configure(state="disable")
window.columnconfigure(0, weight=1)
typing_area.grid(column=0, row=3, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)

window.mainloop()