import UI.TypingTab as ttab
import DAO.FileManager as fm
from common_libs import *


class Register:
    def __init__(self, header, bodyWin, user):
        self.bodyWin = bodyWin
        self.user = user
        self.header = header

        # Configuring the window
        self.bodyWin.rowconfigure(0, weight=5)
        self.bodyWin.rowconfigure(1, weight=1)
        self.bodyWin.rowconfigure(2, weight=1)
        self.bodyWin.rowconfigure(3, weight=1)
        self.bodyWin.rowconfigure(4, weight=1)
        self.bodyWin.rowconfigure(5, weight=1)
        self.bodyWin.rowconfigure(6, weight=1)
        self.bodyWin.rowconfigure(7, weight=1)
        self.bodyWin.rowconfigure(8, weight=10)
        self.bodyWin.columnconfigure(0, weight=1)
        self.bodyWin.columnconfigure(1, weight=1)

        self.salutationLbl = tk.Label(self.bodyWin,
                                      font=('Arial', 16, 'bold'),
                                      text='Salutation :',
                                      fg=FG_CLR,
                                      bg=BG_CLR,
                                      relief=tk.FLAT,
                                      anchor=tk.CENTER)

        self.salutation = ttk.Combobox(self.bodyWin,
                                       font=('Arial', 14),
                                       values=['Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Prof.'],
                                       state='readonly')
        self.salutation.set('Mr.')

        self.firstNameLbl = tk.Label(self.bodyWin,
                                     font=('Arial', 16, 'bold'),
                                     text='First Name* :',
                                     fg=FG_CLR,
                                     bg=BG_CLR,
                                     relief=tk.FLAT,
                                     anchor=tk.CENTER)

        self.firstName = tk.Entry(self.bodyWin,
                                  font=('Arial', 14),
                                  fg=FG_CLR,
                                  bg='#fff',
                                  relief=tk.FLAT)

        self.lastNameLbl = tk.Label(self.bodyWin,
                                    font=('Arial', 16, 'bold'),
                                    text='Last Name* :',
                                    fg=FG_CLR,
                                    bg=BG_CLR,
                                    relief=tk.FLAT,
                                    anchor=tk.CENTER)

        self.lastName = tk.Entry(self.bodyWin,
                                 font=('Arial', 14),
                                 fg=FG_CLR,
                                 bg='#fff',
                                 relief=tk.FLAT)

        self.genderLbl = tk.Label(self.bodyWin,
                                  font=('Arial', 16, 'bold'),
                                  text='Gender* :',
                                  fg=FG_CLR,
                                  bg=BG_CLR,
                                  relief=tk.FLAT,
                                  anchor=tk.CENTER)

        self.gender = ttk.Combobox(self.bodyWin,
                                   values=['Male', 'Female', 'Others'],
                                   font=('Arial', 14),
                                   state='readonly')
        self.gender.set('Male')

        self.dateOfBirthLbl = tk.Label(self.bodyWin,
                                       font=('Arial', 16, 'bold'),
                                       text='Date Of Birth* :',
                                       fg=FG_CLR,
                                       bg=BG_CLR,
                                       relief=tk.FLAT,
                                       anchor=tk.CENTER)

        self.dateOfBirth = tk.Entry(self.bodyWin,
                                    font=('Arial', 14),
                                    fg='#aaa',
                                    bg='#fff',
                                    relief=tk.FLAT)

        self.dateOfBirth.insert(0, 'DD/MM/YYYY')
        self.dateOfBirth.bind('<FocusIn>', lambda _: self.focusIn(_, 'DD/MM/YYYY'))
        self.dateOfBirth.bind('<FocusOut>', lambda _: self.focusOut(_, 'DD/MM/YYYY'))

        self.addressLbl = tk.Label(self.bodyWin,
                                   font=('Arial', 16, 'bold'),
                                   text='Address :',
                                   fg=FG_CLR,
                                   bg=BG_CLR,
                                   relief=tk.FLAT,
                                   anchor=tk.CENTER)

        self.address = tk.Entry(self.bodyWin,
                                font=('Arial', 14),
                                fg=FG_CLR,
                                bg='#fff',
                                relief=tk.FLAT)

        self.emailLbl = tk.Label(self.bodyWin,
                                 font=('Arial', 16, 'bold'),
                                 text='Email* :',
                                 fg=FG_CLR,
                                 bg=BG_CLR,
                                 relief=tk.FLAT,
                                 anchor=tk.CENTER)

        self.email = tk.Entry(self.bodyWin,
                              font=('Arial', 14),
                              fg='#aaa',
                              bg='#fff',
                              relief=tk.FLAT)

        self.email.insert(0, 'abc@company.com')
        self.email.bind('<FocusIn>', lambda _: self.focusIn(_, 'abc@company.com'))
        self.email.bind('<FocusOut>', lambda _: self.focusOut(_, 'abc@company.com'))

        self.nationalityLbl = tk.Label(self.bodyWin,
                                       font=('Arial', 16, 'bold'),
                                       text='Nationality :',
                                       fg=FG_CLR,
                                       bg=BG_CLR,
                                       relief=tk.FLAT,
                                       anchor=tk.CENTER)

        self.nationality = tk.Entry(self.bodyWin,
                                    font=('Arial', 14),
                                    fg=FG_CLR,
                                    bg='#fff',
                                    relief=tk.FLAT)

        self.submitBtn = tk.Button(self.bodyWin,
                                   font=('Arial', 16, 'bold'),
                                   text='Sign Up',
                                   bg=HIGHLIGHT_CLR,
                                   fg='#fff',
                                   activebackground='#fff',
                                   activeforeground=HIGHLIGHT_CLR,
                                   relief=tk.FLAT,
                                   anchor=tk.CENTER,
                                   command=self.submit)

        self.resetBtn = tk.Button(self.bodyWin,
                                  font=('Arial', 16, 'bold'),
                                  text='Clear',
                                  bg=HIGHLIGHT_CLR,
                                  fg='#fff',
                                  activebackground='#fff',
                                  activeforeground=HIGHLIGHT_CLR,
                                  relief=tk.FLAT,
                                  anchor=tk.CENTER,
                                  command=self.reset)

        self.salutationLbl.grid(row=0, column=0, sticky=tk.SE)
        self.salutation.grid(row=0, column=1, sticky=tk.SW)

        self.firstNameLbl.grid(row=1, column=0, sticky=tk.E)
        self.firstName.grid(row=1, column=1, sticky=tk.W)
        self.firstName.bind('<Return>', lambda _: self.submit())

        self.lastNameLbl.grid(row=2, column=0, sticky=tk.E)
        self.lastName.grid(row=2, column=1, sticky=tk.W)
        self.lastName.bind('<Return>', lambda _: self.submit())

        self.genderLbl.grid(row=3, column=0, sticky=tk.E)
        self.gender.grid(row=3, column=1, sticky=tk.W)

        self.dateOfBirthLbl.grid(row=4, column=0, sticky=tk.E)
        self.dateOfBirth.grid(row=4, column=1, sticky=tk.W)
        self.dateOfBirth.bind('<Return>', lambda _: self.submit())

        self.addressLbl.grid(row=5, column=0, sticky=tk.E)
        self.address.grid(row=5, column=1, sticky=tk.W)
        self.address.bind('<Return>', lambda _: self.submit())

        self.emailLbl.grid(row=6, column=0, sticky=tk.E)
        self.email.grid(row=6, column=1, sticky=tk.W)
        self.email.bind('<Return>', lambda _: self.submit())

        self.nationalityLbl.grid(row=7, column=0, sticky=tk.E)
        self.nationality.grid(row=7, column=1, sticky=tk.W)
        self.nationality.bind('<Return>', lambda _: self.submit())

        self.resetBtn.grid(row=8, column=0, sticky=tk.NE, padx=50)
        self.submitBtn.grid(row=8, column=1, sticky=tk.NW, padx=50)
        self.submitBtn.bind('<Return>', lambda _: self.submit())

    def checkEmail(self):
        if (self.email.get() == ''): return False

        temp = self.email.get()
        pattern = r'^[a-zA-Z0-9\._\+\-]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,}$'

        if (re.match(pattern, temp) == None):    return False

        return True

    def checkBOD(self):
        if (self.dateOfBirth.get() == ''): return False

        temp = self.dateOfBirth.get()
        pattern = r'^[0-3][0-9]/[0-1][0-9]/\d{4}$'

        if (re.match(pattern, temp) is None):    return False

        return True

    def submit(self):
        if (self.firstName.get() == '' or
                self.lastName.get() == '' or
                not self.checkEmail() or
                not self.checkBOD()):
            msg.showerror('Missing Data',
                          'Please enter all the mandatory data.')
            return

        self.user.salutation = self.salutation.get().strip()
        self.user.firstName = self.firstName.get().strip()
        self.user.lastName = self.lastName.get().strip()
        self.user.gender = self.gender.get().strip()
        self.user.dateOfBirth = self.dateOfBirth.get().strip()
        self.user.address = self.address.get().strip()
        self.user.email = self.email.get().strip()
        self.user.nationality = self.nationality.get().strip()

        fm.FileManager.saveUser(self.user)
        fm.FileManager.update(self.user)

        msg.showinfo('Successful', 'Account Created Successfully ')

        for widget in self.bodyWin.winfo_children():
            widget.destroy()

        self.header.config(text='Welcome ' + self.user.firstName)

        ttab.TypingTab(self.header, self.bodyWin, self.user)

    def reset(self):
        self.firstName.delete(0, 'end')
        self.lastName.delete(0, 'end')
        self.dateOfBirth.delete(0, 'end')
        self.address.delete(0, 'end')
        self.email.delete(0, 'end')
        self.nationality.delete(0, 'end')

    def focusIn(self, event, placeholder):
        if (event.widget.get() == placeholder):
            event.widget.delete(0, 'end')
            event.widget.config(fg=FG_CLR)

    def focusOut(self, event, placeholder):
        if (event.widget.get() == ''):
            event.widget.insert(0, placeholder)
            event.widget.config(fg='#aaa')
