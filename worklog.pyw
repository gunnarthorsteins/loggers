"""Logs what the user is working on and for how long at a time.

Every second time it logs the starting time and the other time it logs
the time elapsed and the project being worked on.


Version 2.0
"""

import os
import csv
from datetime import datetime
import pandas as pd
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as agg

import widgets
import config

frmt = r'%Y-%m-%d %H:%M'
increment = 0.058
now = datetime.now()


class WorkLog:

    def __init__(self):
        self.ts = 'timestamp.csv'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, tb):
        pass

    def check_timestamp(self):
        """Checks the latest timestamp. If empty then it thrFows
        an EmptyDataError, catched by __exit__ which then writes
        a new timestamp, gives feedback and finally raises SystemExit.
        """

        try:
            df_timestamp = pd.read_csv(self.ts,
                                       header=None)
            # Rewrite the timestamp file as empty
            with open(self.ts, 'w'):
                pass

            return df_timestamp

        except pd.errors.EmptyDataError:
            with open(self.ts,
                      mode='w') as f:
                w = csv.writer(f)
                w.writerow([now])

            self.feedback()

    @staticmethod
    def feedback():
        """Feedback Box for the user to know
        that the logging has successfully started.
        """

        widget = widgets.Widget(config=config.feedback)
        root = widget.root_mkr()
        widget.frm_mkr()

        timestamp = now.strftime(r'%Y-%m-%d %H:%M')
        msg = f'Logging\nStarted\n{timestamp}'
        widget.lbl_mkr(rel_y=0.3,
                       txt=msg,
                       anchor='c')

        root.after(3000, root.destroy)
        root.mainloop()

    @staticmethod
    def log_work():
        """Logs the project being worked on."""

        project = Setup.entry_project.get()
        comment = Setup.entry_comment.get()
        t_start = Setup.entry_start.get()
        t_end = Setup.entry_end.get()

        t_i = datetime.strptime(t_start, frmt)
        t_f = datetime.strptime(t_end, frmt)
        delta = t_f-t_i
        # Somehow there isn't a command for formatting
        # timedeltas like there is strptime for datetimes???
        delta = str(delta) if delta.seconds/3600 > 9 else '0'+str(delta)

        with open('worklog.csv',
                  mode='a') as f:
            w = csv.writer(f,
                           delimiter="\t",
                           lineterminator="\n")
            w.writerow([t_start,
                        t_end,
                        delta,
                        project,
                        comment])
        Setup.root.destroy()

    def sum_month(self):
        """Logs and plots the total hours worked last month."""

        def plot_sum():
            """Bar chart displaying the total hours logged last month."""
            root = tk.Tk()
            root.title('Work Logger')
            df_plt = pd.DataFrame()
            t_logged = pd.to_timedelta(df.elapsed)
            df_plt.insert(0, 'hours', t_logged.dt.seconds/3600)
            df_plt.insert(1, 'project', df.project)
            # Sum the hours by project
            df_plt = df_plt.groupby('project')['hours'].sum()
            fig = plt.Figure(figsize=(7, 6),
                             dpi=100)
            ax = fig.add_subplot(111)
            bar = agg(fig, root)
            bar.get_tk_widget().pack(side=tk.LEFT,
                                     fill=tk.BOTH)
            df_plt.plot(kind='bar',
                        legend=False,
                        ax=ax)
            ax.grid(axis='y')
            ax.set_title('Total hours logged in %s: %.0f'
                         % (st_of_last_mon.strftime('%B'),
                            hours_logged))
            fig.tight_layout()

        # 'encoding' is to parse Icelandic letters
        df = pd.read_csv('worklog.csv',
                         sep='\t',
                         encoding='unicode_escape')
        df.t_i = df.t_i.astype('datetime64[ns]')
        # NOTE It's 2 and 1 because we're referring to last month
        # and this month, respectively.
        offset_2 = pd.offsets.MonthBegin(2, normalize=True)
        offset_1 = pd.offsets.MonthBegin(1, normalize=True)
        st_of_last_mon = now - offset_2
        st_of_this_mon = now - offset_1
        # Filter df to only include last month's entries
        df = df[df.t_i >= st_of_last_mon]
        df = df[df.t_i < st_of_this_mon]
        t_tot = pd.to_timedelta(df.elapsed).sum()
        hours_logged = round(t_tot.total_seconds()/3600, 1)

        plot_sum()

    def manual_entry(self):
        """Opens the log file for editing mistakes in logging."""

        # Note the whitespace following [.exe]
        os.system(f'notepad.exe {os.getcwd()}/worklog.csv')


class Setup:
    """Sets up the widget"""

    def __init__(self):
        print('run')

    def __call__(self):
        w = WorkLog()
        with w as worklog:
            ts_start = worklog.check_timestamp()
            if ts_start is None:
                return

            start = ts_start[0][0]
            rel_y = 0

            # Widget Setup
            widget = widgets.Widget(config=config.worklog)
            Setup.root = widget.root_mkr()
            widget.frm_mkr()

            # Entry Boxes
            # Label: [preallocation for entry box, in-place entry value]
            entries = {'Project': [None, ''],
                       'Comment': [None, ''],
                       'Start': [None, start[:16]],
                       'End': [None, now.strftime(frmt)]}
            for key, val in entries.items():
                widget.lbl_mkr(rel_y=rel_y,
                               txt=key)
                rel_y += increment*0.9
                val[0] = widget.entry_mkr(rel_y=rel_y,
                                          set_focus=True)
                val[0].insert(0, val[1])
                rel_y += increment
            Setup.entry_project = entries['Project'][0]
            Setup.entry_comment = entries['Comment'][0]
            Setup.entry_start = entries['Start'][0]
            Setup.entry_end = entries['End'][0]
            rel_y += increment*0.7

            # Buttons
            btns = {'Log': [(lambda: worklog.log_work()), True],
                    'Sum': [(lambda: worklog.sum_month()), False],
                    'View File': [(lambda: worklog.manual_entry()), False]}
            for key, val in btns.items():
                widget.btn_mkr(rel_y=rel_y,
                               txt=key,
                               fun=val[0],
                               invoke=val[1])
                rel_y += increment*1.3

            # Labels with last projects
            widget.lbl_mkr(rel_y=rel_y,
                           txt='Last 5:')
            rel_y += increment*0.8
            df = pd.read_csv('worklog.csv',
                             sep='\t',
                             encoding='unicode-escape')
            df = df.project
            # Reversing for the unique() command to filter correctly
            df = df.iloc[::-1]
            projects = df.unique()
            projects = projects[:5]
            for project in projects:
                widget.lbl_mkr(rel_y=rel_y,
                               txt='- '+project)
                rel_y += increment*0.8

            Setup.root.mainloop()


if __name__ == '__main__':
    run = Setup()
    run()
