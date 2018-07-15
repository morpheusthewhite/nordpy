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

        self.center_window(300, 160)

        if checkOpenVPN():
            self.setStatusAlreadyConnected()
        else:
            self.setStatusDisconnected()

    def __initOptions__(self):
        self.optionsFrame = LabelFrame(self, text="Options")

        self.serverTypeFrame = Frame(self.optionsFrame)
        self.serverTypeFrame.serverTypeLabel = Label(self.serverTypeFrame, text="Server Type")
        self.serverTypeFrame.serverTypeLabel.pack(side=LEFT, padx=10)
        self.serverType = StringVar(self)
        self.serverType.set("Standard VPN")  # default value
        self.serverTypeFrame.serverTypeMenu = OptionMenu(self.serverTypeFrame, self.serverType, "P2P", "Dedicated IP",
                                                      "Double VPN", "Onion over VPN", "Standard VPN", "Obfuscated")
        self.serverTypeFrame.serverTypeMenu.pack()
        self.serverTypeFrame.pack()

        self.protocolFrame = Frame(self.optionsFrame)
        self.protocolFrame.protocolLabel = Label(self.protocolFrame, text="Protocol: ")
        self.protocolFrame.protocolLabel.pack(side=LEFT)
        self.connectionProtocol = IntVar()
        self.protocolFrame.tcp = Radiobutton(self.protocolFrame, text="TCP", variable=self.connectionProtocol, value=1,
                                             selectcolor="black")
        self.protocolFrame.tcp.pack(side=LEFT)
        self.protocolFrame.udp = Radiobutton(self.protocolFrame, text="UDP", variable=self.connectionProtocol, value=0,
                                             selectcolor="black")
        self.protocolFrame.udp.pack(side=LEFT)
        self.connectionProtocol.set(1)
        self.protocolFrame.pack(pady=6)

        self.optionsFrame.pack(fill="x")

    def __initStatus__(self):
        self.statusFrame = Frame(self)
        self.statusFrame.statusStatic = Label(self.statusFrame, text="Status: ")
        self.statusFrame.statusStatic.pack(side=LEFT)
        self.statusFrame.statusDinamic = Label(self.statusFrame)
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

        self.buttonsFrame.connect.configure(state=ACTIVE)
        self.buttonsFrame.disconnect.configure(state=DISABLED)

    def setStatusConnected(self, serverName, protocol):
        self.statusFrame.statusDinamic.configure(text="Connected to "+serverName + " by " +
                                                      PROTOCOLS[protocol], foreground="green")

        self.buttonsFrame.connect.configure(state=DISABLED)
        self.buttonsFrame.disconnect.configure(state=ACTIVE)

    def setStatusAlreadyConnected(self):
        self.statusFrame.statusDinamic.configure(text="Already connected", foreground="green")

        self.buttonsFrame.connect.configure(state=DISABLED)
        self.buttonsFrame.disconnect.configure(state=ACTIVE)

    def connect(self):
        recommendedServer = getRecommendedServer(self.serverType.get())

        if recommendedServer is None:
            messagebox.showwarning(title="Error", message="Sorry, server not found! Please try a different server.")
            return

        protocolSelected = self.connectionProtocol.get()

        if hasattr(self, "sudoPassword"):
            (self.openvpnProcess, _) = startVPN(recommendedServer, protocolSelected, self.sudoPassword)
        else:
            (self.openvpnProcess, self.sudoPassword) = startVPN(recommendedServer, protocolSelected, None)

        self.setStatusConnected(recommendedServer, protocolSelected)

    def disconnect(self):
        if checkOpenVPN() or self.openvpnProcess.poll() is None:
            if not hasattr(self, "sudoPassword"):
                self.sudoPassword = askRootPassword()

            getRootPermissions(self.sudoPassword)
            subprocess.call(["sudo", "killall", "openvpn"])

        self.setStatusDisconnected()

    def center_window(self, width=300, height=200):
        # gets screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculates position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))