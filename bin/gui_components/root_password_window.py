from tkinter import *
import os
from bin.pathUtil import CURRENT_PATH
from bin.root import test_root_password, wrong_root_password
from bin.gui_components.centered_window import CenteredWindow

password_inserted = None


class RootPermissionWindow(CenteredWindow):
    """
    A window used to require root password before launching NordPy main interface
    """
    def __init__(self):
        """
        Initialize window

        Args:
            self: (todo): write your description
        """
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

        self.center_window(200, 85, font_name=self.ok_button.cget("font"))

    def on_enter_pressed(self, event):
        """
        Enter the keyboard press event handler.

        Args:
            self: (todo): write your description
            event: (todo): write your description
        """
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

