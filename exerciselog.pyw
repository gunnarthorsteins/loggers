"""A program for daily exercise logging.

Logs the duration, type of exercise and has the option to display
summary statistics.

The program is heavily commented as I used it both as an exercise
in Tkinter and -more importantly- an exercise in setting up a program
in compliance with best practices.


Version: 1.0
"""

import os
import csv
import datetime
import pandas as pd
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as agg


class Gui:

    # GUI properties. In this case I believe they should rather be
    # here than inside __init__. See https://bit.ly/3mTsx9n for rationale
    HEIGHT = 1020
    WIDTH = 200
    FONT_SIZE = 20
    REL_H = 0.07
    BD = 10
    SPACE = 0.06
    REL_WIDTH = 0.92
    BORDER = 0
    REL_X = 0.04
    rel_y = 0.02
    bg = '#B9D9EB'  # BackGround: Columbia blue
    font = 'Tahoma'

    def __init__(self):
        """Initiating the GUI."""

        # For the app not to crash if exercise type is not pressed.
        # Maybe it might be weird to declare it here, but it works anyways.
        ExLog.ex_type = None
        ExLog.duration = 0

    def root_mkr(self, title, h, w):
        """Creates a GUI root."""

        Gui.root = tk.Tk()
        Gui.root.title(title)
        canvas = tk.Canvas(Gui.root,
                           height=h,
                           width=w)
        canvas.pack()

        # To position the widget in the center of the screen
        scr_width = Gui.root.winfo_screenwidth()
        scr_height = Gui.root.winfo_screenheight()
        x = scr_width/2 - w/2
        y = scr_height/2 - h/2 - 40
        Gui.root.geometry('+%d+%d' % (x, y))

        return Gui.root

    def frm_mkr(self, root, border=0):
        """Creates a GUI frame."""

        frm = tk.Frame(self.root,
                       bg=self.bg,
                       bd=self.BD)
        frm.place(relx=border,
                  rely=border,
                  relwidth=1-2*border,
                  relheight=1-2*border,
                  anchor='nw')

    def lbl_mkr(self, frm, txt, rel_y,
                rel_h=REL_H, anchor='w', c='#022169'):
        """Creates a GUI label."""

        lab = tk.Label(frm,
                       text=txt,
                       font=(self.font,
                             self.FONT_SIZE,
                             'bold'),
                       anchor=anchor,
                       bg=self.bg,
                       fg=c)
        lab.place(relx=self.REL_X,
                  rely=rel_y,
                  relwidth=self.REL_WIDTH,
                  relheight=rel_h)
        Gui.rel_y += self.SPACE

    def entry_mkr(self, frm, rel_y, set_focus=False):
        """Creates a GUI entry box."""

        entry = tk.Entry(frm,
                         bd=self.BD*0.5,
                         font=(self.font,
                               self.FONT_SIZE))
        entry.place(relx=self.REL_X,
                    rely=rel_y,
                    relwidth=self.REL_WIDTH,
                    relheight=self.REL_H*0.8)
        if set_focus:
            entry.focus_set()
        Gui.rel_y += self.SPACE

        # We return entry bc then we retain the
        # actual entries which we can then log
        return entry

    def btn_mkr(self, frm, key, fun, rel_y, invoke=False):
        """Creates a GUI button."""

        btn = tk.Button(frm,
                        text=key,
                        font=(self.font,
                              self.FONT_SIZE,
                              'italic'),
                        command=fun,
                        anchor='w',
                        bg='#0072CE',
                        fg='white')
        btn.place(relx=self.REL_X,
                  rely=rel_y,
                  relwidth=self.REL_WIDTH,
                  relheight=self.REL_H*0.7)
        Gui.rel_y += self.SPACE*0.9
        # To connect a button to the Enter button on the
        # physical keyboard
        if invoke:
            self.root.bind('<Return>',
                           lambda event=None: btn.invoke())

    def rdbtn_mkr(self, frm, i, key, rel_y, img, kbrd_binding=None):
        """Creates a GUI radiobutton."""

        # Note the parenthesis when calling the lambda function.
        # 'indicatoron=0' is for aesthetic purposes.
        # 'value=i' is for the buttons to be detached,
        # otherwise pressing one will press all of them.
        rdbtn = tk.Radiobutton(frm,
                               indicatoron=0,
                               value=i,
                               font=(self.font,
                                     self.FONT_SIZE),
                               command=lambda: ExLog().rdbtn_val(key),
                               anchor='center',
                               bg='white')
        rdbtn.config(image=img)
        # A necessary line, otherwise the images will be garbage collected
        # See here: https://bit.ly/3ezbKoU
        rdbtn.image = img
        rdbtn.place(relx=self.REL_X,
                    rely=rel_y,
                    relwidth=self.REL_WIDTH,
                    relheight=self.REL_H*1.1)
        rdbtn.deselect()
        Gui.rel_y += self.SPACE*1.4
        if kbrd_binding:
            # Creates a keyboard shortcut for each radiobutton
            self.root.bind(kbrd_binding,
                           lambda event=None: rdbtn.invoke())

    def gui(self):
        """This is where the GUI itself is assembled."""
        
        Gui.main_root = self.root_mkr('Exercise Logger',
                                      self.HEIGHT,
                                      self.WIDTH)

        Gui.main_frm = self.frm_mkr(Gui.main_root,
                                    border=self.BORDER)
        self.lbl_mkr(Gui.main_frm,
                     'Type:',
                     Gui.rel_y)
        # The keys are the exercise types,
        # the values are the keyboard bindings
        ex = {'Cycling': '<F1>',
              'Running': '<F2>',
              'Yoga': '<F3>',
              'Weights': '<F4>',
              'Swimming': '<F5>',
              'Other': '<F6>'}
        # Note the usage of dict.items() for this concise iteration
        for i, (key, val) in enumerate(ex.items()):
            img = tk.PhotoImage(file='./images/'+key+'.png')
            self.rdbtn_mkr(Gui.main_frm,
                           i,
                           key,
                           Gui.rel_y,
                           img,
                           val)

        self.lbl_mkr(Gui.main_frm,
                     'Duration:',
                     Gui.rel_y)
        Gui.entry_1 = self.entry_mkr(Gui.main_frm,
                                     Gui.rel_y,
                                     True)
        # Gui.rel_y += 0.2*self.SPACE
        self.lbl_mkr(Gui.main_frm,
                     'Comment:',
                     Gui.rel_y)
        Gui.entry_2 = self.entry_mkr(Gui.main_frm,
                                     Gui.rel_y,
                                     False)
        Gui.rel_y += 0.1*self.SPACE

        btns = {'Log': (lambda: ExLog().log_ex()),
                'Sum': (lambda: ExLog().sum_month()),
                'Edit Entries': (lambda: ExLog().edit_entries())}
        invoke = [True, False, False]
        for i, (key, val) in enumerate(btns.items()):
            self.btn_mkr(Gui.main_frm,
                         key,
                         val,
                         Gui.rel_y,
                         invoke[i])

        # Runs the GUI - do not touch
        Gui.main_root.mainloop()


# ExLog is a subclass of Gui (see how it inherits from it)
class ExLog(Gui):

    def __init__(self):
        self.cd = 'C:/Users/gunnarth/OneDrive/Documents/' \
                  '5. Misc/Programming/exerciselogger/'

    def rdbtn_val(self, val):
        """Sets the exercise type."""

        ExLog.ex_type = val

    def edit_entries(self):
        """Opens the log file for editing mistakes in logging."""

        # Note the whitespace inside the quote trailing '.exe '
        os.system('notepad.exe ' + self.cd + '/exercise_log.csv')

    def log_ex(self):
        """Logs the exercise."""

        # In the case the user forgets to press the 'Type' button
        # we display a pop-up window with a warning
        if ExLog.ex_type is None:
            root_temp = Gui.root_mkr(self,
                                     'Warning',
                                     300,
                                     500)
            txt = 'Don\'t forget\nto select\nexercise type'
            Gui.lbl_mkr(self,
                        root_temp,
                        txt,
                        rel_y=0,
                        rel_h=0.9,
                        anchor='center',
                        c='red')
            # The time is in milliseconds
            root_temp.after(2000, root_temp.destroy)
            root_temp.mainloop()
            return

        duration = Gui.entry_1.get()
        comment = Gui.entry_2.get()

        # Remove the GUI
        Gui.main_root.destroy()
        dt_form = r'%Y-%m-%d'
        date = datetime.datetime.now()
        with open(self.cd + 'exercise_log.csv',
                  mode='a') as f:
            w = csv.writer(f,
                           delimiter=",",
                           lineterminator="\n")
            w.writerow([date.strftime(dt_form),
                        duration,
                        ExLog.ex_type,
                        comment])

    def sum_month(self, period=2):
        """Sums the exercise statistics for the selected period."""

        # 'encoding' is to parse Icelandic letters
        # format: date,duration,type,comment
        df = pd.read_csv(self.cd + 'exercise_log.csv',
                         encoding='unicode_escape')
        df.date = df.date.astype('datetime64[ns]')
        df.duration = df.duration.astype(float)

        t_curr = datetime.datetime.now()
        # 'period' is the n-th number of past months we'll be looking at
        st_of_last_per = t_curr-pd.offsets.MonthBegin(period,
                                                      normalize=True)
        st_of_this_mon = t_curr-pd.offsets.MonthBegin(1,
                                                      normalize=True)
        # Filter df to only include last period's entries
        df = df[df.date >= st_of_last_per]
        df = df[df.date < st_of_this_mon]

        self.plot_stats(df,
                        grouper='type',
                        cat='hours',
                        st_of_last_per=st_of_last_per)

    def plot_stats(self, df, grouper, cat, st_of_last_per):
        """Bar chart displaying the total exercise hours logged in the selected
        period."""

        root_fig = tk.Tk()
        root_fig.title('Exercise Logger')

        df_plt = pd.DataFrame()
        df_plt.insert(0,
                      cat,
                      df.duration/60)
        df_plt.insert(1,
                      grouper,
                      df.type)
        total_hours = sum(df_plt[cat])
        # Sum the hours by project
        df_plt = df_plt.groupby(grouper)[cat].sum()
        fig = plt.Figure(figsize=(7, 6),
                         dpi=100)
        ax = fig.add_subplot(111)
        bar = agg(fig,
                  root_fig)
        bar.get_tk_widget().pack(side=tk.LEFT,
                                 fill=tk.BOTH)
        df_plt.plot(kind='bar',
                    legend=False,
                    ax=ax)
        ax.grid(axis='y')
        ax.set_title('Total hours logged in %s: %.0f'
                     % (st_of_last_per.strftime('%B'),
                        total_hours))
        fig.tight_layout()


log = Gui()
log.gui()
