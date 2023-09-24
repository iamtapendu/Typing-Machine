class Score:
    def __init__(self):
        self.totalWords = 0
        self.correctWords = 0
        self.timeTaken = 0
        self.accuracy = 0
        self.grossWPM = 0
        self.netWPM = 0

    def setFromRaw(self, tw, flt, sflt, tt):
        self.totalWords = tw
        self.correctWords = tw - flt
        self.timeTaken = tt
        self.accuracy = round((tw - flt - sflt) / tw * 100, 2)
        self.grossWPM = round(tw / tt * 60, 2)
        self.netWPM = round((tw - flt - sflt) / tt * 60, 2)

    def get(self):
        text = {
            'totalWords': self.totalWords,
            'correctWords': self.correctWords,
            'timeTaken': self.timeTaken,
            'accuracy': self.accuracy,
            'grossWPM': self.grossWPM,
            'netWPM': self.netWPM
        }

        return text

    def setFromDict(self, score: dict):
        self.totalWords = int(score['totalWords'])
        self.correctWords = int(score['correctWords'])
        self.timeTaken = int(score['timeTaken'])
        self.accuracy = int(score['accuracy'])
        self.grossWPM = int(score['grossWPM'])
        self.netWPM = int(score['netWPM'])
