
from common_libs import *
import DAO.User as usr


class StatisticTab:
    def __init__(self, header, bodyWin, user):
        self.header = header
        self.bodyWin = bodyWin
        self.user = user

        self.header.config(text=self.user.firstName + ' ' + self.user.lastName)

        self.totalWords = []
        self.correctWords = []
        self.timeTaken = []
        self.accuracy = []
        self.grossWPM = []
        self.netWPM = []
        self.fault = []
        self.level = []
        self.skill = []

        tempUser = usr.User()
        for i in self.user.history:
            self.totalWords.append(i.totalWords)
            self.correctWords.append(i.correctWords)
            self.timeTaken.append(i.timeTaken)
            self.accuracy.append(i.accuracy)
            self.grossWPM.append(i.grossWPM)
            self.netWPM.append(i.netWPM)
            self.fault.append(i.totalWords - i.accuracy / 100 * i.totalWords)

            tempUser.insertHistory(i.totalWords, self.fault[-1], 0, i.timeTaken)
            self.level.append(tempUser.level)
            self.skill.append(tempUser.skillPoint)

        session = range(len(self.accuracy))

        if (len(self.totalWords) != 0):
            avgWords = round(stat.mean(self.totalWords), 2)
            avgAccuracy = round(stat.mean(self.accuracy), 2)
            avgTime = round(stat.mean(self.timeTaken), 2)
            avgFault = round(stat.mean(self.fault), 2)
            avgGrossWPM = round(stat.mean(self.grossWPM), 2)
            avgNetWPM = round(stat.mean(self.netWPM), 2)
        else:
            avgWords = avgAccuracy = avgTime = avgFault = avgGrossWPM = avgNetWPM = 0

        # Configuring the window
        self.bodyWin.rowconfigure(0, weight=1)
        self.bodyWin.rowconfigure(1, weight=9)
        self.bodyWin.columnconfigure(0, weight=1)

        self.fixedFrm = tk.Frame(self.bodyWin, bg=BG_CLR)
        self.vesselFrm = tk.Frame(self.bodyWin, bg=BG_CLR)

        self.fixedFrm.grid(row=0, column=0, sticky=tk.NSEW)
        self.vesselFrm.grid(row=1, column=0, sticky=tk.NSEW)

        self.fixedFrm.rowconfigure(0, weight=1)
        self.fixedFrm.rowconfigure(1, weight=1)
        self.fixedFrm.columnconfigure(0, weight=1)
        self.fixedFrm.columnconfigure(1, weight=1)
        self.fixedFrm.columnconfigure(2, weight=1)

        self.createLable(self.fixedFrm, 'Level : ' + str(self.user.level), 0, 0)
        self.createLable(self.fixedFrm, 'Skill Point : ' + str(self.user.skillPoint), 0, 2)

        self.createLable(self.fixedFrm, 'AVG Net WPM : ' + str(avgNetWPM), 1, 0)
        self.createLable(self.fixedFrm, 'AVG Accuracy : ' + str(avgAccuracy), 1, 1)
        self.createLable(self.fixedFrm, 'AVG Session Time : ' + f'{int(avgTime // 60):02d} : {int(avgTime % 60):02d}',
                         1, 2)

        self.createLable(self.fixedFrm, 'AVG Gross WPM : ' + str(avgGrossWPM), 2, 0)
        self.createLable(self.fixedFrm, 'Fault Rate : ' + str(round(avgFault / avgWords * 100, 2)), 2, 1)
        self.createLable(self.fixedFrm, 'AVG Words Count: ' + str(avgWords), 2, 2)

        # Create a custom style for the progress bar
        custom_style = ttk.Style()
        custom_style.configure("Custom.Horizontal.TProgressbar",
                               troughcolor='#ddd',
                               troughrelief='flat',
                               background='#35cc25',
                               borderwidth=0,
                               barrelief='flat')

        progress = ttk.Progressbar(self.fixedFrm,
                                   orient='horizontal',
                                   length=100,
                                   mode='determinate',
                                   style="Custom.Horizontal.TProgressbar")

        a,b = self.findNxtThresold(self.user.skillPoint)
        progress.step((self.user.skillPoint-a) /(b-a)  * 100)
        progress.grid(row=0, column=1, sticky=tk.NSEW)

        self.vesselFrm.rowconfigure(0, weight=1)
        self.vesselFrm.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.vesselFrm,
                                bg=BG_CLR,
                                height=500,
                                highlightthickness=0,
                                relief=tk.FLAT,
                                bd=0)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        # Create a scrollbar for vertical scrolling
        self.vScrollbar = tk.Scrollbar(self.vesselFrm,
                                       orient="vertical",
                                       bg=BG_CLR,
                                       highlightthickness=0,
                                       bd=0,
                                       width=20,
                                       relief=tk.FLAT,
                                       command=self.canvas.yview)
        self.vScrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Configure the canvas to scroll with the scrollbar
        self.canvas.configure(yscrollcommand=self.vScrollbar.set)

        self.scrFrm = tk.Frame(self.canvas, bg=BG_CLR)
        self.canvas.create_window((0, 0), window=self.scrFrm, anchor=tk.CENTER)

        self.canvas.bind_all('<Button-4>', self.onMouseWheel)
        self.canvas.bind_all('<Button-5>', self.onMouseWheel)

        # Bind the configure event to update the scroll region
        self.scrFrm.bind("<Configure>", self.onConfigure)

        self.frm = []
        for i in range(7):
            self.scrFrm.rowconfigure(i, weight=1)
            for j in range(2):
                self.scrFrm.columnconfigure(j, weight=1)
                self.frm.append(tk.Frame(self.scrFrm, bg=BG_CLR))
                self.frm[-1].grid(row=i, column=j, sticky=tk.NSEW, padx=30, pady=10)

        self.linePlot(session,
                      self.accuracy,
                      'Sessions',
                      'Accuracy',
                      'Accuracy Over Time',
                      self.frm[0])

        self.linePlot(session,
                      self.netWPM,
                      'Sessions',
                      'Net WPM',
                      'Net WPM Over Time',
                      self.frm[1])

        self.linePlot(session,
                      self.grossWPM,
                      'Sessions',
                      'Gross WPM',
                      'Gross WPM Over Time',
                      self.frm[2])

        self.linePlot(session,
                      self.timeTaken,
                      'Sessions',
                      'Duration',
                      'Session Duration Over Time',
                      self.frm[3])

        self.scatterPlot(self.accuracy,
                         self.netWPM,
                         'Accuracy',
                         'Net WPM',
                         'Accuracy vs Net WPM',
                         self.frm[4])

        self.scatterPlot(self.timeTaken,
                         self.netWPM,
                         'Duration',
                         'Net WPM',
                         'Session Duration vs Net WPM',
                         self.frm[5])

        self.scatterPlot(self.timeTaken,
                         self.accuracy,
                         'Duration',
                         'Accuracy',
                         'Session Duration vs Accuracy',
                         self.frm[6])

        self.scatterPlot(self.timeTaken,
                         self.fault,
                         'Duration',
                         'Fault',
                         'Session Duration vs Fault',
                         self.frm[7])

        self.histogram(self.timeTaken,
                       'Duration',
                       'Session Duration',
                       self.frm[8])

        self.histogram(self.totalWords,
                       'Word',
                       'Word Count Distribution',
                       self.frm[9])

        self.histogram(self.netWPM,
                       'Net WPM',
                       'Net WPM Distribution',
                       self.frm[10])

        self.histogram(self.accuracy,
                       'Accuracy',
                       'Accuracy Distribution',
                       self.frm[11])

        self.linePlot(self.skill,
                      self.level,
                      'Skill Point',
                      'Level',
                      'Growth Over Time',
                      self.frm[12])

        self.linePlot(session,
                      self.skill,
                      'Session',
                      'Skill Point',
                      'Skill Point Over Time',
                      self.frm[13])

    def onConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Define the onMouseWheel method to handle scrolling
    def onMouseWheel(self, event):
        if (not self.canvas.winfo_exists()): return
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def createLable(self, frm, text, x, y):
        label = tk.Label(frm,
                         font=('Arial', 16, 'bold'),
                         text=text,
                         fg=FG_CLR,
                         bg=BG_CLR,
                         relief=tk.FLAT,
                         anchor=tk.CENTER)
        label.grid(row=x, column=y, sticky=tk.NSEW)

    def linePlot(self, x, y, x_label, y_label, title, frm):
        fig = plt.Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.plot(x,[stat.mean(y)]*len(y),color='red',label ='Average')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        canvas = bck.FigureCanvasTkAgg(fig, master=frm)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def scatterPlot(self, x, y, x_label, y_label, title, frm):
        fig = plt.Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.scatter(x, y)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        slope, intercept, _, _, _ = st.linregress(x, y)
        rline = [slope * i + intercept for i in x]
        ax.plot(x, rline, color='red',label='Regression Line')
        canvas = bck.FigureCanvasTkAgg(fig, master=frm)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def histogram(self, x, x_label, title, frm):
        fig = plt.Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.hist(x)
        ax.set_xlabel(x_label)
        ax.set_title(title)
        canvas = bck.FigureCanvasTkAgg(fig, master=frm)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def findNxtThresold(self, score):

        a, b = 10, 20
        if (score < a):
            return 0,a
        elif (score < b):
            return a,b
        else:
            while (score >= b):
                a, b = b, a + b

        return a,b
