import DAO.User as usr
from common_libs import *


class FileManager:
    @staticmethod
    def loadUser(user_id=''):
        user = usr.User()

        if (user_id != '' and os.path.exists(DB_PATH + user_id + '.json')):
            temp = FileManager.convertDict(DB_PATH + user_id + '.json')
            if (temp is not None):  user.set(temp)

        elif (os.path.exists(PROFILE_PATH)):
            FileManager.validateProfile()

            userList = None
            with open(PROFILE_PATH) as file:
                userList = file.read().split(',')

            if (userList[-1] != ''):
                temp = FileManager.convertDict(DB_PATH + userList[-1] + '.json')
                if (temp is not None):  user.set(temp)
        else:
            with open(PROFILE_PATH, 'w') as file:
                pass

        return user

    @staticmethod
    def convertDict(path):
        try:
            with open(path) as file:
                dict = json.loads(file.read())
            return dict
        except json.decoder.JSONDecodeError:
            os.remove(path)
            FileManager.validateProfile()
        except FileNotFoundError:
            pass

        return None

    @staticmethod
    def saveUser(user):
        with open(DB_PATH + user.userId + '.json', 'w') as file:
            file.write(str(user))

    @staticmethod
    def update(user):
        lst = None
        try:
            with open(PROFILE_PATH, 'r') as file:
                lst = file.read().split(',')
                if (lst[-1] == ''): lst.pop()

                if (len(lst) != 0):
                    lst.remove(user.userId)

        except FileNotFoundError as e:
            pass

        except ValueError as e:
            pass

        with open(PROFILE_PATH, 'w') as file:
            lst.append(user.userId)
            file.write(','.join(lst))

    @staticmethod
    def loadStory(story_path=''):
        story = story_path

        if (story == ''):
            # listing all the paths of stories
            fileList = [i for i in os.listdir(STORY_PATH) if i.endswith('.txt')]

            story = random.choice(fileList)

        # opening a random story
        with open(STORY_PATH + story) as file:
            # reading the title of the story and displaying in header widget
            header = file.readline().rstrip('\n').strip()

            # reading the whole story and stored as list of words
            content = file.read() \
                .replace('\n', ' ') \
                .split()

        return header, content

    @staticmethod
    def getStories():
        # listing all the paths of stories
        fileList = [i for i in os.listdir(STORY_PATH) if i.endswith('.txt')]
        stories = {}
        for item in fileList:
            with open(STORY_PATH + item) as file:
                heading = file.readline().rstrip('\n').strip()
                stories[heading] = item

        return stories

    @staticmethod
    def loadAudio():
        # initializing pygame mixer for playing sound effects
        pygame.mixer.init(channels=8)

        # loading all the sound effect in a list
        lst = []
        for audio in os.listdir(AUDIO_PATH):
            if audio.endswith('.wav'):
                mixer = pygame.mixer
                lst.append(mixer.Sound(AUDIO_PATH + audio))

        return lst

    @staticmethod
    def validateProfile():
        if (os.path.exists(PROFILE_PATH)):
            with open(PROFILE_PATH) as file:
                lst = file.read().split(',')

                if (lst[-1] == ''): return

                for i in range(len(lst) - 1, -1, -1):
                    if (not os.path.exists(DB_PATH + lst[i] + '.json')):
                        lst.pop(i)

            with open(PROFILE_PATH, 'w') as file:
                file.write(','.join(lst))

    @staticmethod
    def loadRecentUsers():
        users = []
        lst = None

        FileManager.validateProfile()

        with open(PROFILE_PATH) as file:
            lst = file.read().split(',')

        for i in range(len(lst) - 1, -1, -1):
            if (lst[i] == ''): continue

            temp = FileManager.convertDict(DB_PATH + lst[i] + '.json')

            if (temp is None):  continue

            users.append((temp['userId'], temp['firstName']))

        return users

    @staticmethod
    def loadVocabulary():
        content = voc = None
        with open('data/all_words.txt') as file:
            voc = file.read().split(',')
        content = [random.choice(voc) for _ in range(500)]
        return '5. Vocabulary', content

    @staticmethod
    def loadBasicRow():
        content = []
        base = ['a', 's', 'd', 'f', 'j', 'k', 'l', ';']
        for _ in range(500):
            word = ''
            for _ in range(random.randint(3, 5)):
                word += random.choice(base)
            content.append(word)

        return '1. Basic Row', content

    @staticmethod
    def loadHomeRow():
        content = []
        base = ['a', 's', 'd', 'f', 'g', 'j', 'h', 'k', 'l', ';', '\'']
        for _ in range(500):
            word = ''
            for _ in range(random.randint(3, 5)):
                word += random.choice(base)
            content.append(word)

        return '2. Home Row', content

    @staticmethod
    def loadTopRow():
        content = []
        base = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                'a', 's', 'd', 'f', 'g', 'j', 'h', 'k', 'l', ';', '\'']
        for _ in range(500):
            word = ''
            for _ in range(random.randint(3, 5)):
                word += random.choice(base)
            content.append(word)

        return '3. Top Row', content

    @staticmethod
    def loadBottomRow():
        content = []
        base = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                'a', 's', 'd', 'f', 'g', 'j', 'h', 'k', 'l', ';', '\'',
                'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.']
        for _ in range(500):
            word = ''
            for _ in range(random.randint(3, 5)):
                word += random.choice(base)
            content.append(word)

        return '4. Bottom Row', content

    @staticmethod
    def loadNumbers():
        content = []
        base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for _ in range(500):
            word = ''
            for _ in range(random.randint(5, 6)):
                word += random.choice(base)
            content.append(word)

        return '6. Numbers', content
