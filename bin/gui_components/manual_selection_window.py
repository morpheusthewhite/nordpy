from tkinter import *
from os import path
from requests import ConnectionError as RequestsConnectionError

from bin.conf_util import get_available_servers_dict, global_stats_holder
from bin.logging_util import get_logger
from bin.pathUtil import CURRENT_PATH
from bin.gui_components.centered_window import CenteredTopLevel

SERVERS_DICT = get_available_servers_dict()
logger = get_logger(__name__)


class ManualServerWindow(CenteredTopLevel):
    def __init__(self, parent, scale_factor=1):
        """
        Initialize window

        Args:
            self: (todo): write your description
            parent: (todo): write your description
            scale_factor: (array): write your description
        """
        super(ManualServerWindow, self).__init__()
        self.wm_title("Select your server")
        self.parent = parent  # this will be needed when a server is chosen

        # sets the icon
        self.__imgicon__ = PhotoImage(file=path.join(CURRENT_PATH + "media", "manual.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)

        self.__init_listboxes__()
        self.__init_buttons__()

        self.center_window(300, 220, scale_factor, self.accept_button.cget("font"))

        self.grab_set()  # used to disable the underlying window

        # creating stats holder
        try:
            self.stats_holder = global_stats_holder
        except RequestsConnectionError:
            self.stats_holder = None

    def __init_listboxes__(self):
        """
        Initialize all boxes

        Args:
            self: (todo): write your description
        """
        self.listboxes_frame = Frame(self)

        # this frame will contain all the stuff of the domain_listbox
        self.domain_listbox_frame = Frame(self.listboxes_frame)
        self.domain_listbox = Listbox(self.domain_listbox_frame, selectmode=SINGLE)
        self.domain_listbox_frame.scrollbar = Scrollbar(self.domain_listbox_frame, orient=VERTICAL)
        self.domain_listbox.config(yscrollcommand=self.domain_listbox_frame.scrollbar.set)
        self.domain_listbox_frame.scrollbar.config(command=self.domain_listbox.yview)
        self.domain_listbox_frame.scrollbar.pack(side=RIGHT, fill='y')

        # adding keys from SERVERS_DICT
        for item in sorted(SERVERS_DICT.keys()):
            self.domain_listbox.insert(END, item)
        self.domain_listbox.pack(side=RIGHT)
        self.domain_listbox.bind('<<ListboxSelect>>', self.on_domain_select)
        self.domain_listbox_frame.pack(side=LEFT)

        self.domain_servers_listbox_frame = Frame(self.listboxes_frame)
        self.domain_servers_listbox = Listbox(self.domain_servers_listbox_frame, selectmode=SINGLE)
        self.domain_servers_listbox_frame.scrollbar = Scrollbar(self.domain_servers_listbox_frame, orient=VERTICAL)
        self.domain_servers_listbox.config(yscrollcommand=self.domain_servers_listbox_frame.scrollbar.set)
        self.domain_servers_listbox_frame.scrollbar.config(command=self.domain_servers_listbox.yview)
        self.domain_servers_listbox_frame.scrollbar.pack(side=RIGHT, fill='y')
        self.domain_servers_listbox.pack(side=RIGHT)
        self.domain_servers_listbox_frame.pack(side=LEFT)

        self.listboxes_frame.pack()

    def __init_buttons__(self):
        """
        Initialize buttons.

        Args:
            self: (todo): write your description
        """
        self.buttons_frame = Frame(self)
        self.accept_button = Button(self.buttons_frame, text='OK', command=self.ok_pressed)
        self.accept_button.pack(side=LEFT)
        self.cancel_button = Button(self.buttons_frame, text='Cancel', command=self.cancel_pressed)
        self.cancel_button.pack(side=LEFT)
        self.buttons_frame.pack(pady=6)

    def on_domain_select(self, event):
        """
        Insert domain event handler.

        Args:
            self: (todo): write your description
            event: (todo): write your description
        """
        selected_item_tuple = self.domain_listbox.curselection()
        if len(selected_item_tuple) == 0:   # checking if it is a deselection
            return
        selected_index = selected_item_tuple[0]

        domain_selected = self.domain_listbox.get(selected_index)

        self.domain_servers_listbox.delete(0, END)

        if self.stats_holder is None:
            for server in SERVERS_DICT[domain_selected]:
                self.domain_servers_listbox.insert(END, server)
        else:
            for server in SERVERS_DICT[domain_selected]:
                self.domain_servers_listbox.insert(END, server +"  " + self.stats_holder.get_server_stats_as_str(server))


    def ok_pressed(self):
        """
        Destroy the selected item.

        Args:
            self: (todo): write your description
        """
        selected_item_tuple = self.domain_servers_listbox.curselection()
        if not len(selected_item_tuple) == 0:  # checking if something is selected
            selected_index = selected_item_tuple[0]
            server_selected = self.domain_servers_listbox.get(selected_index).split(" ")[0]

            self.parent.manual_server_selected(server_selected)

        self.grab_release()  # to enable again the underlying window
        self.destroy()

    def cancel_pressed(self):
        """
        Cancel the queue. queue.

        Args:
            self: (todo): write your description
        """
        self.grab_release()  # to enable again the underlying window
        self.destroy()

