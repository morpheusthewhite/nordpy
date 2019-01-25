from tkinter import *
from tkinter import messagebox
from bin.pathUtil import *
from bin.credentials import credentials_file_path
from bin.settings import advanced_settings_are_correct, advanced_settings_read, advanced_settings_save

DEFAULT_SCALE_FACTOR = 1

class AdvancedSettingsWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.wm_title("Advanced Settings")

        # sets the icon
        self.__imgicon__ = PhotoImage(file=os.path.join(CURRENT_PATH + "media", "manual.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)

        self.remove_credentials_button = Button(self, text='Reset credentials', command=self.remove_cred)
        self.remove_credentials_button.pack(pady=10)

        self.__init_window_size_frame__()

        self.save_button = Button(self, text="Save", command=self.save_current_settings, height=6)
        self.save_button.pack(ipady=10, pady=10)

        # retrieving existing default configuration
        if(advanced_settings_are_correct()):
            scale_factor = advanced_settings_read()
            self.set_scale(scale_factor)
        else:
            advanced_settings_save(DEFAULT_SCALE_FACTOR)
            self.set_scale(DEFAULT_SCALE_FACTOR)

        self.center_window(300, 150)

        self.grab_set()  # used to disable the underlying window

    def __init_window_size_frame__(self):
        # label above the spinbox
        self.s_label_info = Label(self, text='The following factor affects the width and \nheight'
                                             ' of the main window(not font)')
        self.s_label_info.pack(pady=1)

        # variable for the scale value
        self.scale_var = DoubleVar()

        # frame containing the spinbox
        self.window_size_frame = Frame(self)#, text='Window size')
        self.s_label = Label(self.window_size_frame, text='Scale factor')
        self.s_label.pack(side=LEFT)
        self.scale_sbox = Spinbox(self.window_size_frame, width=6, from_=0.50, increment=0.10, to=3.00,
                                  textvariable=self.scale_var)
        self.scale_sbox.pack(side=LEFT)
        self.window_size_frame.pack()

    def remove_cred(self):
        if messagebox.askyesno(parent=self, title='Confirm', message="Are you sure you want "
                                                                     "to remove stored credentials?"):
            try:
                os.remove(credentials_file_path)
            except FileNotFoundError:
                pass

    def save_current_settings(self):
        advanced_settings_save(self.get_scale())
        messagebox.showinfo(parent=self, title="Restart required", message='Restart the application to apply changes')

    def set_scale(self, n):
        self.scale_var.set(n)

    def get_scale(self):
        return self.scale_var.get()

    def center_window(self, width=300, height=200):
        # gets screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculates position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
