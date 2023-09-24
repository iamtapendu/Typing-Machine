from common_libs import *
import DAO.FileManager as fm


class TypingTab:
    def __init__(self, hdr, bodyWin, user):
        self.header = hdr
        self.bodyWin = bodyWin
        self.user = user
        self.content = ''  # for holding main story
        self.timeTaken = time.time()  # for calculating time
        self.audioList = []  # for holding audio files

        # Configuring the window
        self.bodyWin.rowconfigure(0, weight=20)
        self.bodyWin.rowconfigure(1, weight=75)
        self.bodyWin.rowconfigure(2, weight=5)
        self.bodyWin.columnconfigure(0, weight=1)

        # Text widget for the story to show
        self.paragraph = tk.Text(self.bodyWin,
                                 font=('Arial', 28),
                                 bg=BG_CLR,
                                 fg=FG_CLR,
                                 highlightcolor=BG_CLR,
                                 highlightthickness=0,
                                 relief=tk.FLAT,
                                 height=1,
                                 state=tk.DISABLED)

        # tag for center alignment for normal text
        self.paragraph.tag_config('center', justify='center')

        # tag for center alignment for highlighted text
        self.paragraph.tag_config('bold_center',
                                  justify='center',
                                  font=('Arial', 28, 'bold'),
                                  foreground='#FF3723')

        # Text widget for typing
        self.textArea = tk.Text(self.bodyWin,
                                font=('Arial', 16),
                                bg='#e8e8e8',
                                fg=FG_CLR,
                                highlightcolor='#e8e8e8',
                                highlightthickness=1,
                                relief=tk.FLAT,
                                height=15,
                                state=tk.DISABLED)

        # binding various events
        self.textArea.bind('<Control-c>', lambda _: 'break')  # blocking copy in text area
        self.textArea.bind('<Control-v>', lambda _: 'break')  # blocking paste in text area
        self.textArea.bind('<BackSpace>', lambda _: 'break')  # blocking backspace in text area

        # button for starting type
        self.startBtn = tk.Button(self.bodyWin,
                                  font=('Arial', 20, 'bold'),
                                  text='Start',
                                  bg=HIGHLIGHT_CLR,
                                  fg='#fff',
                                  activebackground='#fff',
                                  activeforeground=HIGHLIGHT_CLR,
                                  relief=tk.FLAT,
                                  anchor=tk.CENTER,
                                  command=self.activate)
        self.stories = fm.FileManager.getStories()
        lstStory = list(self.stories.keys())
        lstStory += ['1. Basic Row', '2. Home Row', '3. Top Row', '4. Bottom Row', '5. Vocabulary', '6. Numbers']
        lstStory.sort(key=lambda x: int(x.split('.')[0]))
        self.textFile = ttk.Combobox(self.bodyWin,
                                     values=lstStory,
                                     font=('Arial', 20),
                                     width=40,
                                     exportselection=False,
                                     state='readonly')
        self.textFile.set(list(self.stories.keys())[0])

        # Label for time elapsed time
        self.time = tk.Label(self.bodyWin,
                             font=('Arial', 20, 'bold'),
                             text='00 : 00',
                             fg=HIGHLIGHT_CLR,
                             bg=BG_CLR,
                             relief=tk.FLAT,
                             anchor=tk.CENTER)

        # flag variable for holding recalling of updateTime method
        self.continueUpdate = False

        # placing the widgets
        self.paragraph.grid(row=0, column=0, sticky=tk.NSEW)
        self.textArea.grid(row=1, column=0, sticky=tk.NSEW)
        self.startBtn.grid(row=2, column=0, sticky=tk.W)
        self.textFile.grid(row=2, column=0, sticky=tk.N, pady=10)
        self.time.grid(row=2, column=0, sticky=tk.E, padx=50)

    # This function will update the elapsed time each second
    def updateTime(self):
        if self.continueUpdate:
            time_ = time.time() - self.timeTaken  # current time - start time

            # Converting to minute and second
            m = int(time_ // 60)
            s = int(time_ % 60)

            # created a formatted string and set the value of the label
            formatted_time = f'{m:02d} : {s:02d}'
            self.time.config(text=formatted_time)

            # recalling the method after each second
            self.time.after(1000, self.updateTime)

    # Event method for updating story, It will show 10 word
    # each time and play the sound effect for each keystroke
    def updatePara(self, event):
        # selecting random audio file and playing it
        random.choice(self.audioList).play()

        # only when space is entered then updating the highlighted text
        if (event.keysym == 'space'):
            # Counting how many words had been typed
            len_ = len(self.textArea.get('1.0', 'end').split())

            # passing the counting to printPara method to highlight the next word
            self.printPara(len_)

    # Method used for printing story in the upper section of the window
    # Highlight is the index of the word that needs to be highlighted
    def printPara(self, highlight=0):
        # changing paragraph to normal state and deleting all its content
        self.paragraph.config(state=tk.NORMAL)
        self.paragraph.delete('1.0', 'end')

        # calculating starting index of story depending upon highlighted word index
        start_loc = highlight // 10 * 10

        # at a time only 10 words are visible
        length = 10 if (len(self.content) > 10 + start_loc) else len(self.content) % 10

        # inserting words in the paragraph widget
        for i in range(start_loc, start_loc + length):
            if (highlight == i):
                self.paragraph.insert('end', self.content[i] + ' ', 'bold_center')
            else:
                self.paragraph.insert('end', self.content[i] + ' ', 'center')

        # disabling the state
        self.paragraph.config(state=tk.DISABLED)

    # entry function when typing starts
    def activate(self):
        # enabling text area for typing and deleting preexisted data
        self.textArea.config(state=tk.NORMAL)
        self.textArea.delete('1.0', 'end')

        # Toggling the start button to act as stop button
        self.startBtn.config(text='Stop', command=self.deactivate)

        # Checking what user picked
        if (self.textFile.get() == '1. Basic Row'):
            header, self.content = fm.FileManager.loadBasicRow()

        elif (self.textFile.get() == '2. Home Row'):
            header, self.content = fm.FileManager.loadHomeRow()

        elif (self.textFile.get() == '3. Top Row'):
            header, self.content = fm.FileManager.loadTopRow()

        elif (self.textFile.get() == '4. Bottom Row'):
            header, self.content = fm.FileManager.loadBottomRow()

        elif (self.textFile.get() == '5. Vocabulary'):
            header, self.content = fm.FileManager.loadVocabulary()

        elif (self.textFile.get() == '6. Numbers'):
            header, self.content = fm.FileManager.loadNumbers()

        else:
            # getting the selected story
            story_path = self.stories[self.textFile.get()]

            # Loading story from stored stories
            header, self.content = fm.FileManager.loadStory(story_path)

        self.header.config(text=header)

        # loading all the sound effect in a list
        self.audioList = fm.FileManager.loadAudio()

        # Binding updatePara to text area for playing sound effect and
        # update paragraph widget dynamically
        self.textArea.bind('<KeyPress>', self.updatePara)

        # pressing <Return> (Enter) key will stop the process
        self.textArea.bind('<Return>', lambda _: self.deactivate())

        # printing the first 10 lines from the story
        self.printPara()

        # setting the focus in the text area
        self.textArea.focus()

        # enabling continueTime method to run periodically
        self.continueUpdate = True

        # initializing timeTaken for first time
        self.timeTaken = time.time()

        # calling updateTime to update time elapsed
        self.updateTime()

    # finding the number of word written by the user
    def findLength(self, userWords):
        fault = length = 0

        # finding user written words count
        # if it's more than original then returning
        # original count and extra count added as fault
        if (len(userWords) <= len(self.content)):
            length = len(userWords)
        else:
            length = len(self.content)
            fault = len(userWords) - length

        return length, fault

    # Function for showing the various values and WPM
    def generateReport(self):
        # extracting words from text area
        userWords = self.textArea.get('1.0', 'end').rstrip().split(' ')
        spaceFault = 0

        # counting if there is more than one space between
        # two words and increasing fault
        for i in range(len(userWords)):
            if (userWords[i] == ''):
                spaceFault += 1

        # extracting words from text area without extra whitespace
        userWords = self.textArea.get('1.0', 'end').split()
        length, fault = self.findLength(userWords)

        # checking for accuracy
        for i in range(length):
            if (userWords[i] != self.content[i]):
                fault += 1

        # if user didn't written anything then return
        if (length == 0):  return

        lv, skill = self.user.level, self.user.skillPoint

        # Storing the data in user profile history
        self.user.insertHistory(length, fault, spaceFault, self.timeTaken)

        # Saving the data
        fm.FileManager.saveUser(self.user)

        # calculating and showing the details by a msg box
        msg.showinfo('Typing Report',
                     'Total Words - ' + str(length) + '\n' +
                     'Correct Words - ' + str(length - fault) + '\n' +
                     'Time Taken - ' + f'{int(self.timeTaken // 60):02d} : {int(self.timeTaken % 60):02d}\n' +
                     'Accuracy - ' + str(round((length - fault - spaceFault) / length * 100, 2)) + ' %\n' +
                     'Gross WPM - ' + str(round(length / self.timeTaken * 60, 2)) + '\n' +
                     'Net WPM - ' + str(round((length - fault - spaceFault) / self.timeTaken * 60, 2)) + '\n' +
                     'WPM - Word Per Minute')

        msg.showinfo('Status Report',
                     'Hi ' + self.user.firstName + ', Here is your Status Report -' +'\n'+
                     'Level : ' + str(lv) + ' -> ' + str(self.user.level) + '\n' +
                     'Skill Point : ' + str(skill) + ' -> ' + str(self.user.skillPoint))

    # deactivate method to stop typing activity
    def deactivate(self):
        # Checking if it's already deactivated
        if (self.paragraph.get(1.0, 'end') == '\n'): return

        # subtracting current time from the starting time
        self.timeTaken = time.time() - self.timeTaken
        self.continueUpdate = False  # stopping updateTime to recall itself

        self.header.config(text='Typing Test')  # changing header

        # deleting the story from widget
        self.paragraph.config(state=tk.NORMAL)
        self.paragraph.delete('1.0', 'end')
        self.paragraph.config(state=tk.DISABLED)

        # preventing from typing anymore by disabling it
        self.textArea.config(state=tk.DISABLED)

        self.generateReport()

        # Unbinding events that are no need
        self.textArea.unbind('<KeyPress>')
        self.textArea.unbind('<Return>')

        # toggling to original state of the start button
        self.startBtn.config(text='Start', command=self.activate)
