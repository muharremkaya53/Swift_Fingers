import tkinter as tk
from TypingApp import TypingApp
from WordLoader import WordLoader

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        wordSource = WordLoader('localhost', 'sam', 'Password1234!', 'typing_test')
        wordSource.connectToDb()
        self.app = TypingApp(self.root, wordSource)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    mainApp = MainApplication()
    mainApp.run()
