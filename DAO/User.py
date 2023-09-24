from common_libs import *
import DAO.Score as sc


class User:
    def __init__(self):
        self.userId = self.generateUserId()
        self.salutation = ''
        self.firstName = ''
        self.lastName = ''
        self.gender = ''
        self.address = ''
        self.dateOfBirth = ''
        self.email = ''
        self.nationality = ''
        self.level = 0
        self.skillPoint = 0
        self.history = []

    def __str__(self):
        text = {
            'userId': self.userId,
            'salutation': self.salutation,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'gender': self.gender,
            'address': self.address,
            'dateOfBirth': self.dateOfBirth,
            'email': self.email,
            'nationality': self.nationality,
            'level': self.level,
            'skillPoint': self.skillPoint,
            'history': [i.get() for i in self.history]
        }

        return str(text).replace("'", '"')

    def calculateLevel(self, score):
        self.skillPoint += int(score.accuracy / 100 * 5 + score.netWPM / 60 * 5 + score.timeTaken / 60 * 3) / 2
        a, b = 10, 20
        if (self.skillPoint <= a):
            self.level = 1
        elif (self.skillPoint <= b):
            self.level = 2
        else:
            count = 3
            while (self.skillPoint > b):
                a, b = b, a + b
                if (self.skillPoint >= b): self.level = count
                count += 1

    def insertHistory(self, tw, flt, sflt, tt):
        score = sc.Score()
        score.setFromRaw(tw, flt, sflt, tt)
        self.calculateLevel(score)
        self.history.append(score)

    def generateUserId(self):
        num = [i for i in os.listdir(DB_PATH) if i.endswith('.json')]

        if (len(num) == 0): return 'user_10001'

        num.sort()

        return 'user_' + str(int(num[-1][-10:-5]) + 1)

    def set(self, user):
        self.userId = user['userId']
        self.salutation = user['salutation']
        self.firstName = user['firstName']
        self.lastName = user['lastName']
        self.gender = user['gender']
        self.address = user['address']
        self.dateOfBirth = user['dateOfBirth']
        self.email = user['email']
        self.nationality = user['nationality']
        self.level = int(user['level'])
        self.skillPoint = int(user['skillPoint'])
        for i in user['history']:
            score = sc.Score()
            score.setFromDict(i)
            self.history.append(score)
