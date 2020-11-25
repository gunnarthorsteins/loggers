import os
import sys
import csv
import datetime
import traceback
import pandas as pd
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as agg


cwd = os.getcwd()


class Worklog:
    """Logs what the user is working on and for how long at a time.

    Every second time it logs the starting time and the other time it logs
    the time elapsed and the project being worked on.
    """

    def __init__(self):
        pass

    def check_timestamp(self):
        """Checks the latest timestamp. If empty then writes a new timestamp,
        gives feedback and finally raises SystemExit.
        """

        try:
            df_timestamp = pd.read_csv(f'{cwd}/timestamp.csv',
                                       header=None)

            return df_timestamp
        except pd.errors.EmptyDataError:
            timestamp = datetime.datetime.now()
            with open(f'{cwd}/timestamp.csv',
                      mode='w') as f:
                w = csv.writer(f)
                w.writerow([timestamp])

            self.feedback(timestamp)
            raise SystemExit

        except Exception:
            print(traceback.format_exc())

    def feedback(self, timestamp):
        # Feedback Box for the user to know
        # that the logging has started
        root_3 = tk.Tk()
        root_3.title('Work Logger')
        canvas = tk.Canvas(root_3,
                           height=300,
                           width=500,
                           bg='#4ffe34')
        canvas.pack()
        timestamp = timestamp.strftime(r'%Y-%m-%d %H:%M')
        message = f'Logging\nHas Commenced\n{timestamp}'
        label = tk.Label(root_3,
                         text=message,
                         font=('Courier',
                               32))
        label.place(relx=0,
                    relwidth=1,
                    relheight=1)
        # The time is in milliseconds
        root_3.after(3000, root_3.destroy)
        root_3.mainloop()

    def log_work():
        """Logs the project being worked on."""

        project = entry_1.get()
        comment = entry_2.get()
        # Remove the pop-up window
        root_1.destroy()
        dt_form = r'%Y-%m-%d %H:%M'
        with open(cwd + 'work_log.csv',
                  mode='a') as f:
            w = csv.writer(f,
                           delimiter=",",
                           lineterminator="\n")
            w.writerow([t_i.strftime(dt_form),
                        t_f.strftime(dt_form),
                        delta,
                        project,
                        comment])

    def sum_month():
        """Logs and plots the total hours worked last month."""

        # 'encoding' is to parse Icelandic letters
        df = pd.read_csv(cwd + 'work_log.csv',
                         encoding='unicode_escape')
        df.t_i = df.t_i.astype('datetime64[ns]')
        # NOTE It's 2 because we're referring to last month
        t_curr = datetime.datetime.now()
        st_of_last_mon = t_curr-pd.offsets.MonthBegin(1,
                                                      normalize=True)
        st_of_this_mon = t_curr-pd.offsets.MonthBegin(0,
                                                      normalize=True)
        # Filter df to only include last month's entries
        df = df[df.t_i >= st_of_last_mon]
        df = df[df.t_i < st_of_this_mon]
        t_tot = pd.to_timedelta(df.elapsed).sum()
        hours_logged = round(t_tot.total_seconds()/3600,
                             1)
        with open(cwd + 'monthly_summation.csv',
                  mode='a') as f:
            w = csv.writer(f,
                           delimiter=',',
                           lineterminator='\n')
            w.writerow([st_of_last_mon.strftime(r'%Y-%m'),
                        hours_logged])
        root_1.destroy()

        # Bar chart displaying the total hours logged last month
        root_2 = tk.Tk()
        root_2.title('Work Logger')
        df_plt = pd.DataFrame()
        t_logged = pd.to_timedelta(df.elapsed)
        df_plt.insert(0, 'hours', t_logged.dt.seconds/3600)
        df_plt.insert(1, 'project', df.project)
        # Sum the hours by project
        df_plt = df_plt.groupby('project')['hours'].sum()
        fig = plt.Figure(figsize=(7, 6),
                         dpi=100)
        ax = fig.add_subplot(111)
        bar = agg(fig,
                  root_2)
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

    def edit_entries():
        """Opens the log file for editing mistakes in logging."""

        # Note the whitespace following [.exe]
        os.system(f'notepad.exe {cwd}/work_log.csv')


if __name__ == '__main__':
    try:
        runtime = Worklog()
        runtime.check_timestamp()
    except Exception:
        # print(e)

        # Rewrite the timestamp file as empty
        with open('timestamp.csv',
                  'w') as f:
            pass

        df = df.astype('datetime64[ns]')
        t_i = df[0][0]
        t_f = datetime.datetime.now()
        delta = t_f-t_i
        # That's a bad line, but if it looks stupid
        # but it works then it ain't stupid
        delta = str(delta).split(".")[0].split(" ")[2]

        # The Input Box
        font_size = 20
        bg = '#80c1ff'
        root_1 = tk.Tk()
        root_1.title('Work Logger')
        canvas = tk.Canvas(root_1,
                           height=300,
                           width=1000)
        canvas.pack()
        frame_1 = tk.Frame(root_1,
                           bg=bg,
                           bd=5)
        frame_1.place(relx=0.5,
                      rely=0.1,
                      relwidth=0.8,
                      relheight=0.2,
                      anchor='n')
        label = tk.Label(frame_1,
                         text=delta.rsplit(":", 1)[0],
                         font=('Courier',
                               font_size))
        label.place(relx=0,
                    relwidth=0.2,
                    relheight=1)
        entry_1 = tk.Entry(frame_1,
                           bd=5,
                           font=('Courier',
                                 font_size))
        entry_1.place(relx=0.2,
                      relwidth=0.3,
                      relheight=1)
        entry_1.focus_set()
        entry_2 = tk.Entry(frame_1,
                           bd=5,
                           font=('Courier',
                                 font_size))
        entry_2.place(relx=0.5,
                      relwidth=0.4,
                      relheight=1)
        button_1 = tk.Button(frame_1,
                             text='Log',
                             width=10,
                             font=('Courier',
                                   font_size),
                             command=log_work)
        button_1.place(relx=0.9,
                       relwidth=0.1,
                       relheight=1)
        # Enable the 'Enter' key
        root_1.bind('<Return>',
                    lambda event=None: button_1.invoke())

        # The Summation Button on the Input Box
        frame_2 = tk.Frame(root_1,
                           bg=bg,
                           bd=5)
        frame_2.place(relx=0.5,
                      rely=0.3,
                      relwidth=0.8,
                      relheight=0.2,
                      anchor='n')
        button_2 = tk.Button(frame_2,
                             text='Sum Last Month',
                             width=10,
                             font=('Courier',
                                   font_size),
                             command=sum_month)
        button_2.place(relx=0.7,
                       relwidth=0.3,
                       relheight=1)

        # The all-important Edit Entries Button on the Input Box
        button_3 = tk.Button(frame_2,
                             text='Edit Entries',
                             width=10,
                             font=('Courier',
                                   font_size),
                             command=edit_entries)
        button_3.place(relx=0,
                       relwidth=0.3,
                       relheight=1)

        root_1.mainloop()
    finally:
        pass
