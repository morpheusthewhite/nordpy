from tkinter import *
from bin.networkSelection import MODES


class OptionFrame(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Automatic Selection")

        self.serverTypeFrame = Frame(self)
        self.serverTypeFrame.serverTypeLabel = Label(self.serverTypeFrame, text="Server Type")
        self.serverTypeFrame.serverTypeLabel.pack(side=LEFT, padx=10)
        self.serverType = StringVar(self)
        self.serverType.set("Standard VPN")  # default value
        self.serverTypeFrame.serverTypeMenu = OptionMenu(self.serverTypeFrame, self.serverType, *MODES)
        self.serverTypeFrame.serverTypeMenu.pack()
        self.serverTypeFrame.pack()

        self.pack(fill="x", pady=10)

    def option_frame_state_change(self, use_manual):
        if not use_manual:
            # enabling option frame
            self.serverTypeFrame.serverTypeLabel.config(state=NORMAL)
            self.serverTypeFrame.serverTypeMenu.config(state=NORMAL)
        else:
            # disabling option frame
            self.serverTypeFrame.serverTypeLabel.config(state=DISABLED)
            self.serverTypeFrame.serverTypeMenu.config(state=DISABLED)

    def get_selected_server(self):
        return self.serverType.get()

    def set_selected_server(self, server):
        self.serverType.set(server)

