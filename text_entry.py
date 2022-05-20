from distutils.log import error
from tkinter import Text as txt, StringVar, END

from sqlalchemy import TEXT

class TextEntry(txt):
    def __init__(self, parent):
        """TextEntry object for typing test
           parent: parent window or frame
        """
        super().__init__(parent)
        
        # create a proxy for the TextEntry widget for onchange event
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.master_text = ""
        self.configure(wrap="word")
        self.bind("<<TextModified>>", self.on_change)
        self.tag_configure("error", foreground="red")
        self.errors = 0
        self.words = 0

    def set_test_text(self, sentences):
        """sets the sentences to compare against"""
        self.master_text = sentences.strip()

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result

    def on_change(self, p):
        """Check text for errors and highlight mistyped words"""
        typed_text = self.get("1.0", END)
        errors = 0
        # Check accuracy after every word
        if typed_text.endswith(" \n"):
            typed_text = typed_text.strip()
            words_initial = typed_text.split(" ")
            
            #remove extra word entries if multiple spaces used but count as error
            words = []
            for word in words_initial:
                if word == "":
                    errors += 1
                else:
                    words.append(word)
            master_words = self.master_text.split(" ")

            for i in range(0, len(words)):
                if words[i] != master_words[i]:
                    errors += 1

            # Tag word if error
            if words[-1] == self.master_text.split(" ")[len(words) - 1]:
                self.tag_remove("error", "1." + str(len(typed_text) - len(words[-1])), "1." + str(len(typed_text)))
            else:
                self.tag_add("error", "1." + str(len(typed_text) - len(words[-1])), "1." + str(len(typed_text)))

            self.errors = errors
            self.words = len(words)

        # Disallow enter key for now
        elif typed_text.endswith("\n\n"):
            self.delete("end-2c", END)

    def get_score(self):
        """Returns tuple object containing number of words typed and number of errors"""
        return (self.words, self.errors)