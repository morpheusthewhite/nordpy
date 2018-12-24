from bin.gui_components.option_frame import *
from bin.gui_components.manual_selection_frame import *
from bin.conf_util import exists_conf_for, update_conf_files
from bin.networkSelection import *
from bin.openvpn import *
from bin.root import askRootPassword
from bin.settings import *
from bin.logging_util import get_logger
from bin.gui_components.manual_selection_frame import DEFAULT_MANUAL_SERVER_LABEL

logger = get_logger(__name__)


class gui(Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("NordPY")

        # sets the icon
        self.__imgicon__ = PhotoImage(file=os.path.join(CURRENT_PATH+"media", "nordvpn.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)
        # getting color for background (some widget will need it)
        self.background_color = self.cget('background')

        self.manual_frame = ManualSelectionFrame(self, self.background_color)
        self.optionsFrame = OptionFrame(self)
        self.__init_protocol__()
        self.__initStatus__()
        self.__initButtons__()

        self.center_window(350, 260)

        if checkOpenVPN():
            self.setStatusAlreadyConnected()
        else:
            self.setStatusDisconnected()

        if exists_saved_settings():
            serverType, protocol, self.previously_recommended_server = load_settings()
            self.optionsFrame.set_selected_server(serverType)
            self.connectionProtocol.set(protocol)

        self.on_manual_change()

    def __initStatus__(self):
        self.statusFrame = Frame(self)
        self.statusFrame.statusStatic = Label(self.statusFrame, text="Status: ")
        self.statusFrame.statusStatic.pack(side=LEFT)
        self.statusFrame.statusDinamic = Label(self.statusFrame)
        self.statusFrame.statusDinamic.pack(side=LEFT)
        self.statusFrame.pack(ipady=10)

    def __init_protocol__(self):
        self.protocolFrame = Frame(self)
        self.protocolFrame.protocolLabel = Label(self.protocolFrame, text="Protocol: ")
        self.protocolFrame.protocolLabel.pack(side=LEFT)
        self.connectionProtocol = IntVar()
        self.protocolFrame.tcp = Radiobutton(self.protocolFrame, text="TCP", variable=self.connectionProtocol, value=1,
                                             selectcolor=self.background_color)
        self.protocolFrame.tcp.pack(side=LEFT)
        self.protocolFrame.udp = Radiobutton(self.protocolFrame, text="UDP", variable=self.connectionProtocol, value=0,
                                             selectcolor=self.background_color)
        self.protocolFrame.udp.pack(side=LEFT)
        self.connectionProtocol.set(1)
        self.protocolFrame.pack(pady=4)


    def __initButtons__(self):
        self.buttonsFrame = Frame(self)
        self.buttonsFrame.connect = Button(text="Connect", command=self.connect)
        self.buttonsFrame.connect.pack(side=LEFT, padx=5)
        self.buttonsFrame.disconnect = Button(text="Disconnect", command=self.disconnect, state=DISABLED)
        self.buttonsFrame.disconnect.pack(side=RIGHT, padx=5)
        self.buttonsFrame.pack()

    def on_manual_change(self):
        self.manual_frame.__manual_frame_state_change__()
        self.optionsFrame.option_frame_state_change(self.manual_frame.get_is_manual())

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

        if not hasattr(self, "sudoPassword"):
            password = askRootPassword()
            if password is None:
                logger.info("No sudo password inserted")
                self.setStatusDisconnected()
                return
            self.sudoPassword = password

        if self.manual_frame.get_is_manual():
            self.manual_connection()
        else:
            self.automatic_connection()

    def manual_connection(self):
        server = self.manual_frame.get_manual_server()
        if server == DEFAULT_MANUAL_SERVER_LABEL:
            messagebox.showwarning(title="Select a server", message='Please select a manual server')
            return
        self.connect_to_VPN(server , self.connectionProtocol.get())

    def automatic_connection(self):
        try:
            recommendedServer = getRecommendedServer(self.optionsFrame.get_selected_server())
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

        # check if recommended server exists. If it does not exists, download the needed files
        if not exists_conf_for(recommendedServer, protocolSelected):
            update_conf_files(self.sudoPassword)

            # if file does not exist then it is incorrect (extreme case)
            if not exists_conf_for(recommendedServer, protocolSelected):
                messagebox.showwarning(title="Error", message="Retrieved a wrong server from NordVPN, try again")
                return

        self.connect_to_VPN(recommendedServer, protocolSelected)

    def connect_to_VPN(self, server, protocol):
        self.setStatusConnecting() # TODO: not always executed

        try:
            self.openvpnProcess = startVPN(server, protocol, self.sudoPassword)

        except ConnectionError:
            messagebox.showwarning(title="Error", message="Error Connecting")
            self.setStatusDisconnected()
            return
        except LoginError:
            messagebox.showwarning(title="Error", message="Wrong credentials")
            os.remove(credentials_file_path)
            return

        self.setStatusConnected(server, protocol)

        update_settings(self.optionsFrame.get_selected_server(), protocol, server)

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
