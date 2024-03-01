class TypingTest:
    def __init__(self):
        self.typedWords = []  
        self.currentWord = ""  

    def feedEvent(self, char):
        if char.isalpha():
            self.currentWord += char

        elif char == '\b':  # Backspace handling
            self.currentWord = self.currentWord[:-1]

        elif char == ' ':
            if self.currentWord:
                self.typedWords.append(self.currentWord)
                print(f"Word added: {self.currentWord}, All words so far: {self.typedWords}")
                self.currentWord = ""
                return True  

        return False

    def compareWords(self, targetWords):
        correctWords = []
        incorrectWords = []

        for typedWord, targetWord in zip(self.typedWords, targetWords):
            if typedWord == targetWord:
                correctWords.append(typedWord)
            else:
                incorrectWords.append(typedWord)

        if len(self.typedWords) < len(targetWords):
            incorrectWords.extend(targetWords[len(self.typedWords):])

        return correctWords, incorrectWords
