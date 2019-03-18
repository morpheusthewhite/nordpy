from tkinter import *
from tkinter import messagebox
from bin.settings import update_settings
from bin.gui_components.advanced_settings_window import AdvancedSettingsWindow

class SettingsFrame(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Settings")
        self.parent = parent

        self.reset_button = Button(self, text='Reset settings', command=self.reset_settings)
        self.reset_button.pack(side=LEFT, padx=30)

        self.advanced_settings = Button(self, text='Advanced settings', command=self.open_advanced_settings)
        self.advanced_settings.pack(side=RIGHT, padx=30)

        self.pack(fill='x', pady=4, ipady=4)

    def reset_settings(self):
        answer = messagebox.askyesno(title='Confirm', message="Are you sure you want to reset connection settings?")
        if answer:
            self.parent.reset_settings()
            update_settings("", 0, "", "")

    def open_advanced_settings(self):
        AdvancedSettingsWindow(self.parent)

