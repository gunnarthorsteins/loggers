"""A program for daily exercise logging.

Logs the duration, type of exercise and has the option to display
summary statistics.
"""

import os
import csv
import subprocess
import pandas as pd
import tkinter as tk
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as agg

import widgets
import config


frmt = config.exercise['DT_FORMAT']
increment = config.exercise['INCREMENT']
now = datetime.now()
SUM_LAST_MONTH = True


class ExLog:
    """Contains the module functionality."""

    def __init__(self):
        pass

    def __enter__(s elf):
        return self

    def __exit__(self, exc_type, exc_val, tb):
        pass

    @staticmethod
    def rdbtn_val(val):
        """Sets the exercise type. Supporting function for
        the radiobuttons.
        """

        ExLog.ex_type = val
        print(ExLog.ex_type)

    def manual_entry(self):
        """Opens the log file for manual entries."""

        subprocess.call(f'{os.getcwd()}/exerciselog.csv',
                        shell=True)

    def log_ex(self):
        """Logs the exercise."""

        def disp_warning():
            """In case of the user forgets to press the 'Type'
            button we display a pop-up window with a warning.
            """

            widget = widgets.Widget(config.warning)
            root_warn = widget.root_mkr()
            widget.frm_mkr()

            txt = 'Don\'t forget\nto select\nexercise type'
            widget.lbl_mkr(rel_y=0.3,
                           txt=txt,
                           anchor='c')

            root_warn.after(2000, root_warn.destroy)
            root_warn.mainloop()

            return

        if ExLog.ex_type is None:
            disp_warning()

        duration = Setup.entry_1.get()
        comment = Setup.entry_2.get()

        # Remove the GUI
        Setup.root.destroy()
        dt_form = r'%Y-%m-%d'
        with open('exerciselog.csv',
                  mode='a') as f:
            w = csv.writer(f,
                           delimiter=",",
                           lineterminator="\n")
            w.writerow([now.strftime(dt_form),
                        duration,
                        ExLog.ex_type,
                        comment])

    def sum_period(self, start=1, end=0):
        """Sums the exercise statistics for the selected period.

        Params:
            start: Start of the period to be summed over, in months
            end: End of the period to be summed over, in months.

        Example:
            sum_period(start=1, end=0) -> Sums this month
        """

        def plot_stats(grouper, cat):
            """Bar chart displaying the total exercise
            hours logged in the selected period."""

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

        # 'encoding' is to parse Icelandic letters
        df = pd.read_csv('exerciselog.csv',
                         encoding='unicode_escape')
        df.date = df.date.astype('datetime64[ns]')
        df.duration = df.duration.astype(float)

        offset_2 = pd.offsets.MonthBegin(start, normalize=True)
        offset_1 = pd.offsets.MonthBegin(end, normalize=True)
        st_of_last_per = now - offset_2
        st_of_this_per = now - offset_1
        # Filter df to only include last period's entries
        df = df[df.date >= st_of_last_per]
        df = df[df.date < st_of_this_per]

        plot_stats(grouper='type',
                   cat='hours')


class Setup:
    """Contains the widget setup."""

    def __init__(self):
        # For the app not to crash if exercise type is not pressed.
        # Maybe it might be weird to declare it here, but it works anyways.
        ExLog.ex_type = None
        ExLog.duration = 0

    def __call__(self):
        e = ExLog()
        with e as exercise:
            widget = widgets.Widget(config=config.exercise)
            Setup.root = widget.root_mkr()
            widget.frm_mkr()

            rel_y = 0
            widget.lbl_mkr(rel_y=rel_y,
                           txt='Type')
            rel_y += increment*0.9
            ex = {'Cycling': '<F1>',
                  'Running': '<F2>',
                  'Yoga': '<F3>',
                  'Weights': '<F4>',
                  'Swimming': '<F5>',
                  'Other': '<F6>'}
            for key, val in ex.items():
                img = tk.PhotoImage(file=f'./images/{key}.png')
                widget.rdbtn_mkr(rel_y=rel_y,
                                 key=key,
                                 img=img,
                                 lambda_fun=ExLog.rdbtn_val(key),
                                 kbrd_binding=val)
                rel_y += increment*1.4

            widget.lbl_mkr(rel_y=rel_y,
                           txt='Duration')
            rel_y += increment*0.8
            Setup.entry_1 = widget.entry_mkr(rel_y=rel_y,
                                             set_focus=True)
            rel_y += increment*0.9
            widget.lbl_mkr(rel_y=rel_y,
                           txt='Comment')
            rel_y += increment*0.8
            Setup.entry_2 = widget.entry_mkr(rel_y=rel_y,
                                             set_focus=False)
            rel_y += increment*1.4

            btns = {'Log': [(lambda: exercise.log_ex()), True],
                    'Sum': [(lambda: exercise.sum_period()), False],
                    'Manual': [(lambda: exercise.manual_entry()), False]}
            for key, val in btns.items():
                widget.btn_mkr(rel_y=rel_y,
                               txt=key,
                               fun=val[0],
                               invoke=val[1])
                rel_y += increment*1.1

            Setup.root.mainloop()


if __name__ == '__main__':
    run = Setup()
    run()
