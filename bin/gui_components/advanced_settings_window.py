from tkinter import *
from tkinter import messagebox
from bin.pathUtil import *
from bin.credentials import credentials_file_path
from bin.settings import advanced_settings_are_correct, advanced_settings_read, advanced_settings_save
from bin.root import get_root_permissions
from bin.font_size import get_font_scale_factor

DEFAULT_SCALE_FACTOR = 1
DEFAULT_NM_USE = False


class AdvancedSettingsWindow(Toplevel):
    def __init__(self, main_gui, scale_factor=1):
        super().__init__()
        self.wm_title("Advanced Settings")
        self.main_gui = main_gui
        self.scale_factor = scale_factor

        # sets the icon
        self.__imgicon__ = PhotoImage(file=os.path.join(CURRENT_PATH + "media", "manual.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)

        self.remove_credentials_button = Button(self, text='Reset credentials', command=self.remove_cred)
        self.remove_credentials_button.pack(pady=10)

        self.__init_scale_factor_frame__()
        self.__init_nm_frame__()

        self.save_button = Button(self, text="Save", command=self.save_current_settings, height=6)
        self.save_button.pack(ipady=10, pady=10)

        # retrieving existing default configuration
        if(advanced_settings_are_correct()):
            (scale_factor, nm_use) = advanced_settings_read()
            self.set_scale(scale_factor)
            self.set_nm_use(nm_use)
        else:
            advanced_settings_save(DEFAULT_SCALE_FACTOR, DEFAULT_NM_USE)
            self.set_scale(DEFAULT_SCALE_FACTOR)
            self.set_nm_use(DEFAULT_NM_USE)

        self.center_window(300 * scale_factor, 160 * scale_factor, self.save_button.cget("font"))

        self.grab_set()  # used to disable the underlying window

    def __init_scale_factor_frame__(self):
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

    def __init_nm_frame__(self):
        # getting background color from window background (needed by checkbox)
        background_color = self.cget('background')

        # initializing checkbutton variable
        self.nm_use = BooleanVar()

        self.nm_checkbutton = Checkbutton(self, text='Use Network Manager if possible',
                                          selectcolor=background_color, variable=self.nm_use)
        self.nm_checkbutton.pack(pady=8)

    def remove_cred(self):
        if not get_root_permissions(parent=self):
            return

        if messagebox.askyesno(parent=self, title='Confirm', message="Are you sure you want "
                                                                     "to remove stored credentials?"):
            try:
                os.remove(credentials_file_path)
            except FileNotFoundError:
                pass

    def save_current_settings(self):
        advanced_settings_save(self.get_scale(), self.get_nm_use())
        self.main_gui.update_advanced_settings(self.get_nm_use())
        messagebox.showinfo(parent=self, title="Restart required", message='Restart the application to apply scale')

    def set_scale(self, n):
        self.scale_var.set(n)

    def get_scale(self):
        return self.scale_var.get()

    def get_nm_use(self):
        return self.nm_use.get()

    def set_nm_use(self, use):
        self.nm_use.set(use)

    def center_window(self, width=300, height=200, font_name='TkDefaultFont'):
        # gets screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        font_factor = get_font_scale_factor(font_name)

        # calculates position x and y coordinates
        x = (screen_width / 2) - (width * font_factor / 2)
        y = (screen_height / 2) - (height * font_factor / 2)
        self.geometry('%dx%d+%d+%d' % (width * font_factor, height * font_factor, x, y))
