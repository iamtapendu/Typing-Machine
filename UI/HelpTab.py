import tkinter

from common_libs import *


class HelpTab:
    def __init__(self, bodyWin):
        self.bodyWin = bodyWin

        self.bodyWin.rowconfigure(0, weight=1)
        self.bodyWin.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.bodyWin,
                                bg=BG_CLR,
                                height=720,
                                highlightthickness=0,
                                relief=tk.FLAT,
                                bd=0)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        # Create a scrollbar for vertical scrolling
        self.vScrollbar = tk.Scrollbar(self.bodyWin,
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

        # Bind the configure event to update the scroll region
        self.scrFrm.bind("<Configure>", self.onConfigure)

        self.canvas.bind_all('<Button-4>', self.onMouseWheel)
        self.canvas.bind_all('<Button-5>', self.onMouseWheel)

        self.scrFrm.columnconfigure(0, weight=1)

        img = ImageTk.PhotoImage(Image.open('data/help.png'))
        self.pic = tk.Label(self.scrFrm, image=img, bg=BG_CLR, anchor=tk.CENTER)
        self.pic.image = img

        self.pic.grid(row=0, column=0, sticky=tk.NSEW, padx=440)

        text = ''
        with open('data/help_text.txt') as file:
            text = file.read()

        self.helpText = tk.Label(self.scrFrm,
                                 font=('Arial', 14),
                                 text=text,
                                 fg=FG_CLR,
                                 bg=BG_CLR,
                                 relief=tk.FLAT,
                                 justify='left',
                                 wraplength=1250)
        self.helpText.grid(row=1, column=0, sticky=tk.NSEW)

    def onConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Define the onMouseWheel method to handle scrolling
    def onMouseWheel(self, event):
        if(not self.canvas.winfo_exists()): return

        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
