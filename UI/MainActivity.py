import UI.TypingTab as ttab
import UI.Register as reg
import UI.StatisticTab as stab
import UI.HelpTab as htab
import DAO.FileManager as fm
import DAO.User as usr
from common_libs import *


class MainActivity(tk.Tk):
    def __init__(self):
        # ------------------------ Window Configure ------------------------
        super().__init__()
        self.title('Typing Machine')
        self.geometry('1280x720')
        self.config(bg=BG_CLR)
        self.protocol('WM_DELETE_WINDOW', self.onClosing)
        # member for user data
        self.user = fm.FileManager.loadUser()

        style = ttk.Style()
        style.configure('TCombobox',
                        relief=tk.FLAT)
        style.map("TCombobox",
                  fieldbackground=[('readonly', '#fff')],
                  selectbackground=[('readonly', '#fff')],
                  selectforeground=[('readonly', FG_CLR)])

        # ------------------------ Main Menu Configure ------------------------

        self.mainMenu = tk.Menu(self,
                                bg=ACT_CLR,
                                fg=BG_CLR,
                                activebackground=BG_CLR,
                                activeforeground=ACT_CLR,
                                activeborderwidth=0,
                                font=('Helvetica', 11, 'bold'),
                                tearoff=0,
                                bd=0, relief=tk.FLAT)

        self.config(menu=self.mainMenu)

        self.account = tk.Menu(self.mainMenu,
                               bg=BG_CLR,
                               fg=FG_CLR,
                               activebackground='#e2e2e2',
                               activeforeground=FG_CLR,
                               activeborderwidth=0,
                               font=('Helvetica', 11, 'bold'),
                               tearoff=0,
                               bd=0, relief=tk.FLAT)

        self.mainMenu.add_cascade(label='Account', menu=self.account)
        self.account.add_command(label='Create Account', command=self.createUser)
        self.account.add_separator()

        self.mainMenu.bind('<Button-1>', lambda _: self.refreshUsers())

        self.mainMenu.add_command(label='Typing Test', command=self.typingTab)
        self.mainMenu.add_command(label='Stats', command=self.statsTab)
        self.mainMenu.add_command(label='Help', command=self.helpTab)

        # ------------------------ Frames Configure ------------------------

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=99)
        # self.rowconfigure(2,weight=1)
        self.columnconfigure(0, weight=1)

        self.headerFrm = tk.Frame(self, bg=BG_CLR)
        self.bodyFrm = tk.Frame(self, bg=BG_CLR)

        self.headerFrm.grid(row=0, column=0, sticky=tk.NSEW)
        self.bodyFrm.grid(row=1, column=0, sticky=tk.NSEW)

        self.headerFrm.rowconfigure(0, weight=1)
        self.headerFrm.columnconfigure(0, weight=1)

        # ------------------------ Header Configure ------------------------

        self.header = tk.Label(self.headerFrm,
                               font=('Helvetica', 20, 'bold'),
                               bg=BG_CLR,
                               fg=ACT_CLR,
                               highlightcolor=BG_CLR,
                               highlightthickness=1,
                               relief=tk.FLAT,
                               anchor=tk.CENTER)
        self.header.grid(row=0, column=0, sticky=tk.NSEW)

        self.checkStatus()

    # ------------------------ Typing Tab ------------------------
    def typingTab(self):
        if (self.user.firstName == ''):
            msg.showwarning('Attention', 'You haven\'t Sign Up yet\n' +
                            'Please create a account to proceed further.')
            return

        for widget in self.bodyFrm.winfo_children():
            widget.destroy()

        self.header.config(text='Welcome ' + self.user.firstName)

        ttab.TypingTab(self.header, self.bodyFrm, self.user)

    # ------------------------ Stats Tab  ------------------------
    def statsTab(self):
        if (self.user.firstName == ''):
            msg.showwarning('Attention', 'You haven\'t Sign Up yet\n' +
                            'Please create a account to proceed further.')
            return

        for widget in self.bodyFrm.winfo_children():
            widget.destroy()

        self.header.config(text='Statistics')
        stab.StatisticTab(self.header,self.bodyFrm,self.user)

    def createUser(self):
        for widget in self.bodyFrm.winfo_children():
            widget.destroy()

        if (self.user.firstName != ''):
            fm.FileManager.saveUser(self.user)
            fm.FileManager.update(self.user)
            self.user = usr.User()

        self.header.config(text='Create Account')

        reg.Register(self.header, self.bodyFrm, self.user)

    def helpTab(self):
        if (self.user.firstName == ''):
            msg.showwarning('Attention', 'You haven\'t Sign Up yet\n' +
                            'Please create a account to proceed further.')
            return

        for widget in self.bodyFrm.winfo_children():
            widget.destroy()

        self.header.config(text='Help')
        htab.HelpTab(self.bodyFrm)

    def checkStatus(self):
        if (self.user.firstName == ''):
            self.createUser()
        else:
            self.typingTab()

    def assignUser(self, user_id=''):
        self.user = fm.FileManager.loadUser(user_id)
        fm.FileManager.update(self.user)
        self.typingTab()

    def refreshUsers(self):
        for i in range(self.account.index('end'), 1, -1):
            self.account.delete(i)

        userList = fm.FileManager.loadRecentUsers()
        for id, name in userList:
            self.account.add_command(label=name, command=lambda x=id: self.assignUser(x))

    def onClosing(self):
        if msg.askyesno("Quit", "Do you want to quit?"):
            if (self.user.firstName != ''):
                fm.FileManager.saveUser(self.user)
                fm.FileManager.update(self.user)
            self.destroy()
