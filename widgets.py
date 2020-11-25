import tkinter as tk


class Widget:
    """"Contains all the necessary methods to set up a
    functional widget. Is optimized for a 'vertical'
    (i.e. one-column) layout.

    Param:
        config (dict): For setting various properties
                       (see config.py)
    Note:
        All properties are listed in config.py
    """

    def __init__(self, config):
        self.props = config
        self.i = 0  # See class method rdbtn_maker()

    def root_mkr(self):
        """Creates a GUI root. Should be the first method called
        after creating an instance of the class.

        Returns:
            'tkinter.Tk' -> to call root.mainloop() & root.destroy
        """

        def center_widget():
            """Places the widget in the center of the
            screen, irrelevant of screen size.
            """

            scr_width = self.root.winfo_screenwidth()
            scr_height = self.root.winfo_screenheight()
            x = scr_width/2 - self.props['W']/2
            # The '40' is a personal preference
            y = scr_height/2 - self.props['H']/2 - 40
            self.root.geometry('+%d+%d' % (x, y))

        self.root = tk.Tk()
        self.root.title(self.props['TITLE'])
        # Brings to front and focus
        self.root.iconify()
        self.root.update()
        self.root.deiconify()

        canvas = tk.Canvas(self.root,
                           height=self.props['H'],
                           width=self.props['W'])
        canvas.pack()
        center_widget()

        return self.root

    def frm_mkr(self, rel_w=1, rel_h=1):
        """Creates a GUI frame. Should be the
        second method called when creating the widget, after root_mkr().

        Params:
            rel_w (float) 
            rel_h (float)
        """

        self.frame = tk.Frame(self.root,
                              bg=self.props['BACKGROUND_COLOR'],
                              bd=self.props['BORDER'])
        self.frame.place(relx=self.props['BORDER'],
                         rely=self.props['BORDER'],
                         relwidth=rel_w-2*self.props['BORDER'],
                         relheight=rel_h-2*self.props['BORDER'],
                         anchor='nw')

    def lbl_mkr(self, rel_y, txt, anchor='w'):
        """Creates a GUI label.

        Params:
            rel_y (float): The label's normalized relative vertical position.
            txt (str): The text to be displayed on the label.
            rel_h (float): The normalized relative label height.
            anchor: ['n', 'e', 's', 'w']
        """

        lab = tk.Label(self.frame,
                       text=txt,
                       font=(self.props['FONT'],
                             self.props['FONT_SIZE'],
                             'bold'),
                       anchor=anchor,
                       bg=self.props['BACKGROUND_COLOR'],
                       fg=self.props['FONT_COLOR'])
        lab.place(relx=self.props['REL_X'],
                  rely=rel_y,
                  relwidth=self.props['REL_W'],
                  relheight=self.props['REL_H']*0.8)

    def entry_mkr(self, rel_y, set_focus=False):
        """Creates a GUI entry box.

        Params:
            rel_y (float): The entry's normalized relative vertical position.
            set_focus (bool): Whether this entry box is the default typing one.

        Returns:
            entry ('tkinter.Entry'): call entry.get() to
                                     collect the actual entries.
        """

        entry = tk.Entry(self.frame,
                         bd=5,
                         font=(self.props['FONT'],
                               self.props['FONT_SIZE']),
                         fg=self.props['BACKGROUND_COLOR'])
        entry.place(relx=self.props['REL_X'],
                    rely=rel_y,
                    relwidth=self.props['REL_W'],
                    relheight=self.props['REL_H']*0.8)
        if set_focus:
            entry.focus_set()

        return entry

    def btn_mkr(self, rel_y, txt, fun, invoke=False):
        """Creates a GUI button.

        Params:
            rel_y (float): The button's normalized relative vertical position.
            key (str): The text displayed on the button.
            fun (): A reference to a lambda function.
            invoke (bool): Whether pressing <Return> will activate the button.

        Example:
            btns = {'Log': [True, (lambda: log_ex())],
                    'Sum': [False, (lambda: sum_month())],
                    'Edit Entries': [False, (lambda: edit_entries())]}
            for key, val in btns.items():
                btn_mkr(rel_y=rel_y,
                        txt=key,
                        fun=val[1],
                        invoke=val[0])
        """

        btn = tk.Button(self.frame,
                        text=txt,
                        font=(self.props['FONT'],
                              self.props['FONT_SIZE'],
                              'italic',
                              'bold'),
                        command=fun,
                        anchor='w',
                        bg=self.props['BUTTON_COLOR'],
                        fg=self.props['BACKGROUND_COLOR'],
                        borderwidth=4)
        btn.place(relx=self.props['REL_X'],
                  rely=rel_y,
                  relwidth=self.props['REL_W'],
                  relheight=self.props['REL_H']*0.8)
        # To connect a button to the Enter button on the physical keyboard
        if invoke:
            self.root.bind('<Return>',
                           lambda event=None: btn.invoke())

    def rdbtn_mkr(self, rel_y, key, img, kbrd_binding=None):
        """Creates a GUI radiobutton.

        Params:
            rel_y (float): The radiobutton's normalized
                           relative vertical position.
            key (str): The image name reference
            img (tk.PhotoImage): It must be low resolution.
            kbrd_binding (str): A representation of the keyboard binding to be
                                attached to the radiobutton.

        Example:
            ex = {'Cycling': '<F1>',
                  'Running': '<F2>',
                  'Yoga': '<F3>',
                  'Weights': '<F4>',
                  'Swimming': '<F5>',
                  'Other': '<F6>'}
            for key, val in ex.items():
                img = tk.PhotoImage(file=f'./images/{key}.png')
                self.rdbtn_mkr(rel_y=rel_y,
                               key=key,
                               img=img,
                               kbrd_binding=val)
        """

        # NOTE the parenthesis when calling the lambda function.
        # 'indicatoron=0' is for aesthetic purposes.
        # 'value=i' is for the buttons to be detached,
        # otherwise pressing one will press all of them
        # (note the incrementation of i in the next logical line)
        rdbtn = tk.Radiobutton(self.frame,
                               indicatoron=0,
                               value=self.i,
                               font=(self.props['FONT'],
                                     self.props['FONT_SIZE']),
                               command=lambda: self.rdbtn_val(key),
                               anchor='center',
                               bg='white')
        self.i += 1
        rdbtn.config(image=img)
        # A necessary line, otherwise the images will be garbage collected.
        # See here: https://bit.ly/3ezbKoU
        rdbtn.image = img
        rdbtn.place(relx=self.props['REL_X'],
                    rely=rel_y,
                    relwidth=self.props['REL_W'],
                    relheight=Widget.self.props['REL_H']*1.1)
        rdbtn.deselect()
        if kbrd_binding:
            # Creates a keyboard shortcut for each radiobutton
            Widget.root.bind(kbrd_binding,
                             lambda event=None: rdbtn.invoke())

    def rdbtn_val(self, val):
        """Sets the exercise type.

        A necessary support function for rdbtn_mkr().
        """

        ex_type = val

        return ex_type

    def gen_line(self):
        pass
