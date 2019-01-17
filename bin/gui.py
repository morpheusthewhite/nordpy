from bin.gui_components.option_frame import *
from bin.gui_components.manual_selection_frame import *
from bin.conf_util import exists_conf_for, update_conf_files
from bin.vpn_util.networkSelection import *
from bin.settings import existing_corrected_saved_settings, load_settings, update_settings
from requests import ConnectionError
from bin.vpn_util.vpn import *

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

        self.center_window(350, 290)

        running_vpn = get_running_vpn()
        if running_vpn is not None:
            self.setStatusAlreadyConnected(running_vpn)
            self.running_connection = running_vpn
        else:
            self.setStatusDisconnected()
            self.running_connection = None

        if existing_corrected_saved_settings():
            serverType, protocol, country, self.previously_recommended_server = load_settings()

            print(protocol)
            self.optionsFrame.set_selected_server(serverType)
            self.connectionProtocol.set(protocol)
            self.optionsFrame.set_selected_country(country)

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
        self.protocolFrame.ikev2 = Radiobutton(self.protocolFrame, text='Ikev2/IPsec', variable=self.connectionProtocol,
                                               value=2, selectcolor=self.background_color)
        self.protocolFrame.ikev2.pack(side=LEFT)
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

    def setStatusAlreadyConnected(self, running_protocol):
        self.statusFrame.statusDinamic.configure(text="Connected by "+running_protocol, foreground="green")

        self.buttonsFrame.connect.configure(state=DISABLED)
        self.buttonsFrame.disconnect.configure(state=ACTIVE)

    def setStatusConnecting(self):
        self.statusFrame.statusDinamic.configure(text="Connecting", foreground="white")

    def connect(self):
        if self.manual_frame.get_is_manual():
            self.manual_connection()
        else:
            self.automatic_connection()

    def manual_connection(self):
        server = self.manual_frame.get_manual_server()
        if server == DEFAULT_MANUAL_SERVER_LABEL:
            messagebox.showwarning(title="Select a server", message='Please select a manual server')
            return
        self.connect_to_VPN(server, self.connectionProtocol.get())

    def automatic_connection(self):
        selected_server_type = self.optionsFrame.get_selected_server()
        selected_country = self.optionsFrame.get_selected_country()

        try:
            recommended_server = get_recommended_server(selected_server_type, selected_country)
            self.previously_recommended_server = recommended_server
        except RequestException:
            messagebox.showinfo(title="Info", message="Connection with nordvpn failed, using last server")
            recommended_server = self.previously_recommended_server
        except ConnectionError:
            messagebox.showerror(title="Error", message="No connection available, please reconnect and try again")
            return

        if recommended_server is None:
            messagebox.showwarning(title="Error", message="Sorry, server not found! Please try a different server.")
            return

        protocol_selected = self.connectionProtocol.get()

        # check if recommended server exists. If it does not exists, download the needed files
        if protocol_selected != 2 and not exists_conf_for(recommended_server, protocol_selected):
            update_conf_files()

            # if file does not exist then it is incorrect (extreme case)
            if not exists_conf_for(recommended_server, protocol_selected):
                messagebox.showwarning(title="Error", message="Retrieved a wrong server from NordVPN, try again")
                return

        # saving settings for the next opening
        update_settings(selected_server_type, protocol_selected, selected_country, recommended_server)

        self.connect_to_VPN(recommended_server, protocol_selected)

    def connect_to_VPN(self, server, protocol):
        self.setStatusConnecting()
        self.update_idletasks()

        try:
            startVPN(server, protocol)

        except ConnectionError:
            messagebox.showwarning(title="Error", message="Error Connecting")
            self.setStatusDisconnected()
            return
        except LoginError:
            messagebox.showwarning(title="Error", message="Wrong credentials")
            os.remove(credentials_file_path)
            return

        if protocol == IKEV2_PROTOCOL_NUMBER:
            self.running_connection = IPSEC_CONNECTION_STRING
        else:
            self.running_connection = OPENVPN_CONNECTION_STRING

        self.setStatusConnected(server, protocol)

    def disconnect(self):
        stop_vpn(self.running_connection)
        self.setStatusDisconnected()

    def center_window(self, width=300, height=200):
        # gets screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculates position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

