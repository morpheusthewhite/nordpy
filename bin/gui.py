from tkinter import *
from bin.networkSelection import *
from bin.openvpn import *
from bin.root import askRootPassword
from bin.settings import *
from bin.networkSelection import MODES
from bin.logging_util import get_logger

logger = get_logger(__name__)


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

        self.center_window(350, 160)

        if checkOpenVPN():
            self.setStatusAlreadyConnected()
        else:
            self.setStatusDisconnected()

        if exists_saved_settings():
            serverType, protocol, self.previously_recommended_server = load_settings()
            self.serverType.set(serverType)
            self.connectionProtocol.set(protocol)

    def __initOptions__(self):
        self.optionsFrame = LabelFrame(self, text="Options")

        self.serverTypeFrame = Frame(self.optionsFrame)
        self.serverTypeFrame.serverTypeLabel = Label(self.serverTypeFrame, text="Server Type")
        self.serverTypeFrame.serverTypeLabel.pack(side=LEFT, padx=10)
        self.serverType = StringVar(self)
        self.serverType.set("Standard VPN")  # default value
        self.serverTypeFrame.serverTypeMenu = OptionMenu(self.serverTypeFrame, self.serverType, *MODES)
        self.serverTypeFrame.serverTypeMenu.pack()
        self.serverTypeFrame.pack()

        self.protocolFrame = Frame(self.optionsFrame)
        self.protocolFrame.protocolLabel = Label(self.protocolFrame, text="Protocol: ")
        self.protocolFrame.protocolLabel.pack(side=LEFT)
        self.connectionProtocol = IntVar()
        # getting color for background
        select_color = self.serverTypeFrame.serverTypeLabel.cget('background')
        self.protocolFrame.tcp = Radiobutton(self.protocolFrame, text="TCP", variable=self.connectionProtocol, value=1,
                                             selectcolor=select_color)
        self.protocolFrame.tcp.pack(side=LEFT)
        self.protocolFrame.udp = Radiobutton(self.protocolFrame, text="UDP", variable=self.connectionProtocol, value=0,
                                             selectcolor=select_color)
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
        self.statusFrame.statusDinamic.configure(text="Connected to " + serverName + " by " +
                                                      PROTOCOLS[protocol], foreground="green")

        self.buttonsFrame.connect.configure(state=DISABLED)
        self.buttonsFrame.disconnect.configure(state=ACTIVE)

    def setStatusAlreadyConnected(self):
        self.statusFrame.statusDinamic.configure(text="Already connected", foreground="green")

        self.buttonsFrame.connect.configure(state=DISABLED)
        self.buttonsFrame.disconnect.configure(state=ACTIVE)

    def setStatusConnecting(self):
        self.statusFrame.statusDinamic.configure(text="Connecting", foreground="white")

    def connect(self):
        try:
            recommendedServer = getRecommendedServer(self.serverType.get())
            self.previously_recommended_server = recommendedServer
        except RequestException:
            messagebox.showinfo(title="Info", message="Connection with nordvpn failed, using last server")
            recommendedServer = self.previously_recommended_server
        except requests.exceptions.ConnectionError:
            messagebox.showerror(title="Error", message="No connection available, please reconnect and try again")
            return

        if recommendedServer is None:
            messagebox.showwarning(title="Error", message="Sorry, server not found! Please try a different server.")
            return

        protocolSelected = self.connectionProtocol.get()

        self.setStatusConnecting() # TODO: not always executed

        try:
            if not hasattr(self, "sudoPassword"):
                password = askRootPassword()
                if password is None:
                    logger.info("No sudo password inserted")
                    self.setStatusDisconnected()
                    return
                self.sudoPassword = password

            self.openvpnProcess = startVPN(recommendedServer, protocolSelected, self.sudoPassword)

        except ConnectionError:
            messagebox.showwarning(title="Error", message="Error Connecting")
            self.setStatusDisconnected()
            return
        except LoginError:
            messagebox.showwarning(title="Error", message="Wrong credentials")
            os.remove(credentials_file_path)
            return

        self.setStatusConnected(recommendedServer, protocolSelected)

        update_settings(self.serverType.get(), protocolSelected, recommendedServer)

    def disconnect(self):
        if checkOpenVPN() or self.openvpnProcess.poll() is None:
            if not hasattr(self, "sudoPassword"):
                tmp = askRootPassword()

                if tmp is None:
                    return

                self.sudoPassword = tmp

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