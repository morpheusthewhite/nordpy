from tkinter import messagebox
from tkinter import *
from bin.networkSelection import *
from bin.openvpn import *


class gui(Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("NordPY")

        # sets the icon
        self.__imgicon__ = PhotoImage(file=os.path.join(CURRENT_PATH+"media", "nordvpn.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)

        self.__initOptions__()
        self.__initStatus__()
        self.__initButtons__()

        self.center_window(300, 140)

    def __initOptions__(self):
        self.optionsFrame = LabelFrame(self, text="Options")
        self.optionsFrame.serverTypeLabel = Label(self.optionsFrame, text="Server Type")
        self.optionsFrame.serverTypeLabel.pack(side=LEFT, padx=10)
        self.serverType = StringVar(self)
        self.serverType.set("Standard VPN")  # default value
        self.optionsFrame.serverTypeMenu = OptionMenu(self.optionsFrame, self.serverType, "P2P", "Dedicated IP",
                                                      "Double VPN", "Onion over VPN", "Standard VPN", "Obfuscated")
        self.optionsFrame.serverTypeMenu.pack()
        self.optionsFrame.pack(fill="x")

    def __initStatus__(self):
        self.statusFrame = Frame(self)
        self.statusFrame.statusStatic = Label(self.statusFrame, text="Status: ")
        self.statusFrame.statusStatic.pack(side=LEFT)
        self.statusFrame.statusDinamic = Label(self.statusFrame)
        self.setStatusDisconnected()
        self.statusFrame.statusDinamic.pack(side=LEFT)
        self.statusFrame.pack(ipady=10)

    def __initButtons__(self):
        self.buttonsFrame = Frame(self)
        self.buttonsFrame.connect = Button(text="Connect", command=self.connect)
        self.buttonsFrame.connect.pack(side=LEFT, padx=5)
        self.buttonsFrame.disconnect = Button(text="Disconnect", command=self.disconnect, state=DISABLED)
        self.buttonsFrame.disconnect.pack(side=RIGHT, padx=5)
        self.buttonsFrame.pack()

    def setStatusDisconnected(self):
        self.statusFrame.statusDinamic.configure(text="Disconnected", foreground="grey")

    def setStatusConnected(self, serverName):
        self.statusFrame.statusDinamic.configure(text="Connected to "+serverName, foreground="green")

    def connect(self):
        recommendedServer = getRecommendedServer(self.serverType.get())

        if recommendedServer is None:
            messagebox.showwarning(title="Error", message="Sorry, server not found! Please try a different server.")
            return

        if hasattr(self, "sudoPassword"):
            (self.openvpnProcess, _) = startVPN(recommendedServer, self.sudoPassword)
        else:
            (self.openvpnProcess, self.sudoPassword) = startVPN(recommendedServer, None)

        self.setStatusConnected(recommendedServer)

        self.buttonsFrame.connect.configure(state=DISABLED)
        self.buttonsFrame.disconnect.configure(state=ACTIVE)

    def disconnect(self):
        if self.openvpnProcess.poll() is None:
            getRootPermissions(self.sudoPassword)
            subprocess.call(["sudo", "killall", "openvpn"])

        self.setStatusDisconnected()

        self.buttonsFrame.connect.configure(state=ACTIVE)
        self.buttonsFrame.disconnect.configure(state=DISABLED)

    def center_window(self, width=300, height=200):
        # gets screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculates position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))