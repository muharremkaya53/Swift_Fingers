import tkinter as tk
from TypingTest import TypingTest
from WordLoader import WordLoader
from TypingStatistics import TypingStatistics

class TypingApp:
    def __init__(self, root, wordSource):
        self.ui = root
        self.ui.title("Swift Fingers")

        self.typingTest = TypingTest()
        self.remainingTime = 30  
        self.timerRunning = False

        self.wordLoader = wordSource
        self.currentDifficulty = "easy"
        self.words = self.wordLoader.getWords()

        self.correctWords = []
        self.incorrectWords = []
        self.wordCounter = 0

        self.typingStats = TypingStatistics()
        self.currentWpm = 0
        self.averageWpm = 0
        self.currentAccuracy = 0
        self.averageAccuracy = 0

        self.setupUI()

    def setupUI(self):
        # Create and place UI components
        self.metricsFrame = tk.Frame(self.ui)
        self.metricsFrame.pack(side=tk.TOP, fill=tk.X)

        self.speedLabelWidget = tk.Label(self.metricsFrame, text="Speed: 0 wpm", anchor="w")
        self.speedLabelWidget.pack(side=tk.LEFT, padx=5)
        
        self.accuracyLabelWidget = tk.Label(self.metricsFrame, text="Accuracy: 0%", anchor="w")
        self.accuracyLabelWidget.pack(side=tk.LEFT, padx=5)

        self.dailyGoalLabelWidget = tk.Label(self.metricsFrame, text="Daily Goal: 0/30 minutes", anchor="e")
        self.dailyGoalLabelWidget.pack(side=tk.RIGHT, padx=5)

        self.timerLabelWidget = tk.Label(self.metricsFrame, text="30", font=("Ubuntu", 16))
        self.timerLabelWidget.pack(side=tk.RIGHT, padx=5)

        self.lessonTextWidget = tk.Text(self.ui, height=10, width=50, wrap="word")
        self.lessonTextWidget.pack(pady=10)
        self.lessonTextWidget.insert(tk.END, ' '.join(self.words))

        self.userInputWidget = tk.Entry(self.ui, font=("Ubuntu", 16), width=50)
        self.userInputWidget.pack(ipady=5)
        self.userInputWidget.bind('<KeyPress>', self.keyPressed)

        self.newTestButton = tk.Button(self.ui, text="Start New Test", command=self.startNewTest)
        self.newTestButton.pack(pady=10)
        self.newTestButton.config(state='disabled')  

    def keyPressed(self, event):
        if not self.timerRunning:
            self.startTest()
            self.timerRunning = True

        wordCompleted = self.typingTest.feedEvent(event.char) 
        if wordCompleted:
            self.userInputWidget.delete(0, tk.END)  
            self.wordCounter += 1

    def endTest(self):
        self.correctWords, self.incorrectWords = self.typingTest.compareWords(self.words[:self.wordCounter])
        self.timerRunning = False
        self.userInputWidget.config(state='disabled')
        print(f"Correct Words: {self.correctWords}, Incorrect Words: {self.incorrectWords}")
        self.calculateStats(len(self.correctWords), self.wordCounter)
        self.updateGUI()
        self.newTestButton.config(state='normal')

    def calculateStats(self, correctCount, totalCount):
        self.typingStats.updateStatistics(correctCount, totalCount)
        self.currentWpm = self.typingStats.calculateCurrentWpm()
        self.averageWpm = self.typingStats.calculateAverageWpm()
        self.currentAccuracy = self.typingStats.calculateCurrentAccuracy()
        self.averageAccuracy = self.typingStats.calculateAverageAccuracy()

    def startTest(self):
        self.timerRunning = True
        self.startTimer()

    def startTimer(self):
        if self.remainingTime > 0:
            self.timerLabelWidget.config(text=str(self.remainingTime))
            self.remainingTime -= 1
            self.ui.after(1000, self.startTimer)
        else:
            self.timerLabelWidget.config(text="Time's up!")
            self.endTest()

    def updateGUI(self):
        self.speedLabelWidget.config(text=f"Speed: {self.currentWpm} wpm")
        self.accuracyLabelWidget.config(text=f"Accuracy: {self.currentAccuracy}%")
        dailyGoalProgress = min(self.typingStats.totalTimeSeconds / (30 * 60), 1) 
        self.dailyGoalLabelWidget.config(text=f"Daily Goal: {dailyGoalProgress:.0%}")  

    def startNewTest(self):
        self.remainingTime = 30  
        self.timerLabelWidget.config(text="10")
        self.wordCounter = 0
        self.correctWords = []
        self.incorrectWords = []
        self.typingTest.typedWords = []

        if self.currentWpm > 5 and self.currentAccuracy > 5:
            if self.currentDifficulty == "easy":
                self.currentDifficulty = "normal"
            elif self.currentDifficulty == "normal":
                self.currentDifficulty = "difficult"

        self.words = self.wordLoader.getWords(self.currentDifficulty)
        self.lessonTextWidget.delete(1.0, tk.END)
        self.lessonTextWidget.insert(tk.END, ' '.join(self.words))

        self.userInputWidget.config(state='normal')
        self.userInputWidget.delete(0, tk.END)

        self.newTestButton.config(state='disabled')

        self.typingStats.resetCurrentSessionStats()
        self.updateGUI()

        self.timerRunning = False
        self.startTest()  

    