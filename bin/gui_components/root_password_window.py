from tkinter import *
import os
from bin.pathUtil import CURRENT_PATH
from bin.root import test_root_password, wrong_root_password
from bin.font_size import get_font_scale_factor

password_inserted = None


class RootPermissionWindow(Tk):
    """
    A window used to require root password before launching NordPy main interface
    """
    def __init__(self):
        super().__init__()
        self.wm_title("NordPY")

        # sets the icon
        self.__imgicon__ = PhotoImage(file=os.path.join(CURRENT_PATH+"media", "nordvpn.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)

        # info text
        self.top_frame = Frame(self)
        self.password_text = Label(self.top_frame, text='Please insert root password:')
        self.password_text.pack()
        self.top_frame.pack(ipady=2, pady=3)

        # field to insert password
        self.middle_frame = Frame(self)
        self.password_field = Entry(self, show="*", width=15)
        self.password_field.pack()
        self.password_field.focus_set()
        self.middle_frame.pack(ipady=3)

        # ok button
        self.lower_frame = Frame(self)
        self.ok_button = Button(self.lower_frame, text='Ok', command=self.on_button_pressed, width=6)
        self.ok_button.pack()
        self.lower_frame.pack(ipady=3)

        # binding enter button to on_button_pressed function
        self.bind('<Return>', self.on_enter_pressed)

        self.center_window(200, 85, self.ok_button.cget("font"))

    def on_enter_pressed(self, event):
        self.on_button_pressed()

    def on_button_pressed(self):
        """
        function triggered by button press
        """
        global password_inserted
        password_inserted = self.password_field.get()
        if test_root_password(password_inserted):
            self.destroy()
        else:
            password_inserted = None
            wrong_root_password()
            self.password_field.delete(0, END)

    def center_window(self, width=300, height=200, font_name='TkDefaultFont'):
        # gets screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        font_factor = get_font_scale_factor(font_name)

        scaled_height = height * font_factor
        scaled_width = width * font_factor

        # calculates position x and y coordinates
        x = (screen_width / 2) - (scaled_width / 2)
        y = (screen_height / 2) - (scaled_height / 2)
        self.geometry('%dx%d+%d+%d' % (scaled_width, scaled_height, x, y))

