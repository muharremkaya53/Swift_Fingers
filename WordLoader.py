import mysql.connector

class WordLoader:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connectToDb(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as error:
            print(f"Error connecting to MySQL database: {error}")

    def closeDb(self):
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()

    def getWords(self, difficulty="easy"):
        if not self.connection:
            print("Not connected to the database.")
            return []

        wordCounts = {
            "easy": {"easy": 20, "normal": 25, "difficult": 5},
            "normal": {"easy": 15, "normal": 30, "difficult": 5},
            "hard": {"easy": 10, "normal": 25, "difficult": 15}
        }

        counts = wordCounts.get(difficulty, wordCounts["easy"])

        query = f"""
        (SELECT word FROM words WHERE level = 'easy' ORDER BY RAND() LIMIT {counts["easy"]})
        UNION ALL
        (SELECT word FROM words WHERE level = 'normal' ORDER BY RAND() LIMIT {counts["normal"]})
        UNION ALL
        (SELECT word FROM words WHERE level = 'difficult' ORDER BY RAND() LIMIT {counts["difficult"]});
        """
        print(f"Executing query for difficulty level '{difficulty}': {query}") 

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                words = [item[0] for item in cursor.fetchall()]
                return words
        except mysql.connector.Error as error:
            print(f"Error fetching words from MySQL database: {error}")
            return []