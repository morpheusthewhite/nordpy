from queue import Queue

from bin.gui_components.option_frame import *
from bin.gui_components.manual_selection_frame import *
from bin.conf_util import exists_conf_for, update_conf_files
from bin.vpn_util.networkSelection import *
from bin.settings import existing_corrected_saved_settings, load_settings, update_settings, \
    advanced_settings_read, advanced_settings_are_correct
from requests import ConnectionError as RequestsConnectionError
from bin.vpn_util.vpn import *
from bin.gui_components.settings_frame import SettingsFrame
from bin.gui_components.advanced_settings_window import DEFAULT_NM_USE
from bin.gui_components.centered_window import CenteredWindow, DEFAULT_SCALE_FACTOR
import threading

logger = get_logger(__name__)

DEFAUL_WIDTH = 370
DEFAUL_HEIGHT = 370


class gui(CenteredWindow):
    def __init__(self):
        super().__init__()
        self.wm_title("NordPY")
        
        # sets the icon
        self.__imgicon__ = PhotoImage(file=os.path.join(CURRENT_PATH+"media", "nordvpn.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)
        # getting color for background (some widget will need it)
        self.background_color = self.cget('background')

        if advanced_settings_are_correct():
            (self.scale_factor, self.nm_use) = advanced_settings_read()
        else:
            (self.scale_factor, self.nm_use) = (DEFAULT_SCALE_FACTOR, DEFAULT_NM_USE)

        self.settings_frame = SettingsFrame(self, self.scale_factor)
        self.manual_frame = ManualSelectionFrame(self, self.background_color, self.scale_factor)
        self.optionsFrame = OptionFrame(self)
        self.__init_protocol__()
        self.__initStatus__()
        self.__initButtons__()

        self.center_window(DEFAUL_WIDTH, DEFAUL_HEIGHT, self.scale_factor, self.optionsFrame.cget("font"))

        running_vpn = get_running_vpn()
        if running_vpn is not None:
            self.setStatusAlreadyConnected(running_vpn)
            self.running_connection = running_vpn
        else:
            self.setStatusDisconnected()
            self.running_connection = None

        if existing_corrected_saved_settings():
            serverType, protocol, country, self.previously_recommended_server = load_settings()

            self.optionsFrame.set_selected_server(serverType)
            self.connectionProtocol.set(protocol)
            self.optionsFrame.set_selected_country(country)

        self.on_manual_change()

        # queue used to communicate with secondary thread
        self.queue = Queue()

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
        if(IPSEC_EXISTS):
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
                                                      protocol, foreground="green")

        self.buttonsFrame.connect.configure(state=DISABLED)
        self.buttonsFrame.disconnect.configure(state=ACTIVE)

    def setStatusAlreadyConnected(self, running_protocol):
        self.statusFrame.statusDinamic.configure(text="Connected by "+running_protocol, foreground="green")

        self.buttonsFrame.connect.configure(state=DISABLED)
        self.buttonsFrame.disconnect.configure(state=ACTIVE)

    def setStatusConnecting(self):
        self.statusFrame.statusDinamic.configure(text="Connecting", foreground="white")

    def set_status_requesting(self):
        self.statusFrame.statusDinamic.configure(text="Retrieving recommended server", foreground="white")

    def connect(self):
        if not get_root_permissions():
            return

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

        # launching thread
        parallel_request = threading.Thread(target=self.parallel_get_recommended_server,
                                            args=(self, selected_server_type, selected_country))
        parallel_request.start()

        # updating gui
        self.set_status_requesting()
        self.update_idletasks()

        parallel_request.join()
        recommended_server = self.queue.get_nowait()

        if recommended_server == "RequestException":
            messagebox.showinfo(title="Info", message="Connection with nordvpn failed, using last server")
            recommended_server = self.previously_recommended_server
        elif recommended_server == "RequestsConnectionError":
            messagebox.showerror(title="Error", message="No connection available, please reconnect and try again")
            self.setStatusDisconnected()
            return

        if recommended_server is None:
            messagebox.showwarning(title="Error", message="Sorry, server not found! Please try a different server.")
            self.setStatusDisconnected()
            return

        protocol_selected = self.connectionProtocol.get()

        # check if recommended server exists. If it does not exists, download the needed files
        if protocol_selected != IKEV2_PROTOCOL_NUMBER and \
                not exists_conf_for(recommended_server, protocol_selected):
            update_conf_files()

            # if file does not exist then it is incorrect (extreme case)
            if not exists_conf_for(recommended_server, protocol_selected):
                messagebox.showwarning(title="Error", message="Retrieved a wrong server from NordVPN, try again")
                return

        # saving settings for the next opening
        update_settings(selected_server_type, protocol_selected, selected_country, recommended_server)

        self.connect_to_VPN(recommended_server, protocol_selected)

    def parallel_get_recommended_server(self, gui, selected_server_type, selected_country):
        """
        function executed by secondary thread to require recommended server
        """
        try:
            result = get_recommended_server(selected_server_type, selected_country)
        except RequestException:
            result = 'RequestException'
        except RequestsConnectionError:
            result = 'RequestsConnectionError'

        gui.queue.put_nowait(result)

    def connect_to_VPN(self, server, protocol):
        self.setStatusConnecting()
        self.update_idletasks()

        try:
            connected_to = startVPN(server, protocol, self.nm_use)

        except ConnectionError:
            messagebox.showwarning(title="Error", message="Error Connecting")
            self.setStatusDisconnected()
            return
        except LoginError:
            messagebox.showwarning(title="Error", message="Wrong credentials")
            os.remove(credentials_file_path)
            self.setStatusDisconnected()
            return
        except OpenresolvError:
            messagebox.showwarning(title="Error", message="Openresolv is missing, run install.sh")
            self.setStatusDisconnected()
            return

        if connected_to == IPSEC_CONNECTION_STRING:
            self.running_connection = IPSEC_CONNECTION_STRING
        elif connected_to == OPENVPN_CONNECTION_STRING:
            self.running_connection = OPENVPN_CONNECTION_STRING
        elif connected_to == NM_CONNECTION_STRING:
            self.running_connection = NM_CONNECTION_STRING
        else: # connected_to is None
            self.setStatusDisconnected()
            return

        self.setStatusConnected(server, self.running_connection)

    def disconnect(self):
        if not get_root_permissions():
            return

        stop_vpn(self.running_connection)
        self.setStatusDisconnected()

    def reset_settings(self):
        self.optionsFrame.set_selected_country(AUTOMATIC_CHOICE_STRING)
        self.optionsFrame.set_selected_server('Standard VPN')
        self.manual_frame.set_is_manual(False)
        self.on_manual_change()

    def update_advanced_settings(self, nm_use):
        self.nm_use = nm_use

