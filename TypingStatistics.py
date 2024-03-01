class TypingStatistics:
    def __init__(self):
        self.correctWordCount = 0
        self.totalWordCount = 0
        self.totalTimeSeconds = 0
        self.sessionDurationSeconds = 30  

    def updateStatistics(self, correct, total):
        self.currentCorrect = correct 
        self.currentTotal = total
        self.correctWordCount += correct
        self.totalWordCount += total
        self.totalTimeSeconds += self.sessionDurationSeconds

    def calculateCurrentWpm(self):
        return self.currentCorrect * 2  # 30 seconds is half a minute

    def calculateAverageWpm(self):
        if self.totalTimeSeconds > 0:
            minutes = self.totalTimeSeconds / 60
            return (self.correctWordCount) / minutes
        else:
            return 0

    def calculateCurrentAccuracy(self):
        if self.currentTotal > 0:
            return (self.currentCorrect / self.currentTotal) * 100
        else:
            return 0

    def calculateAverageAccuracy(self):
        if self.totalWordCount > 0:
            return (self.correctWordCount / self.totalWordCount) * 100
        else:
            return 0
        
    def resetCurrentSessionStats(self):
        self.currentCorrect = 0
        self.currentTotal = 0
        