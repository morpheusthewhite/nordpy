from tkinter import *
from bin.vpn_util.networkSelection import MODES, COUNTRIES


class OptionFrame(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Automatic Selection")

        self.__init_server_type__()
        self.__init_country__()

        self.pack(fill="x", pady=10)

    def __init_server_type__(self):
        # setting up first line containing server type
        self.serverTypeFrame = Frame(self)
        self.serverTypeLabel = Label(self.serverTypeFrame, text="Server Type")
        self.serverTypeLabel.pack(side=LEFT, padx=10)
        self.serverType = StringVar(self)
        self.serverType.set("Standard VPN")  # default value
        self.serverTypeMenu = OptionMenu(self.serverTypeFrame, self.serverType, *MODES)
        self.serverTypeMenu.pack()
        self.serverTypeFrame.pack()

    def __init_country__(self):
        # setting up second line containing country
        self.country_frame = Frame(self)
        self.country_label = Label(self.country_frame, text='Country')
        self.country_label.pack(side=LEFT, padx=10)
        self.country = StringVar(self)
        self.country.set(COUNTRIES["Automatic"][0])  # default value

        # setting up menu
        self.country_menu_button = Menubutton(self.country_frame, textvariable=self.country, indicatoron=True)
        self.continent_menu = Menu(self.country_menu_button, tearoff=False)
        self.country_menu_button.configure(menu=self.continent_menu)

        for continent in COUNTRIES.keys():
            single_continent_menu = Menu(self.continent_menu, tearoff=False)

            self.continent_menu.add_cascade(label=continent, menu=single_continent_menu)

            continent_countries = COUNTRIES[continent]
            continent_countries.sort()
            for value in continent_countries:
                single_continent_menu.add_radiobutton(label=value, variable=self.country, value=value)

        self.country_menu_button.pack()

        self.country_frame.pack()

    def option_frame_state_change(self, use_manual):
        if not use_manual:
            # enabling option frame
            self.serverTypeLabel.config(state=NORMAL)
            self.serverTypeMenu.config(state=NORMAL)
            self.country_menu_button.config(state=NORMAL)
            self.country_label.config(state=NORMAL)
        else:
            # disabling option frame
            self.serverTypeLabel.config(state=DISABLED)
            self.serverTypeMenu.config(state=DISABLED)
            self.country_menu_button.config(state=DISABLED)
            self.country_label.config(state=DISABLED)

    def get_selected_server(self):
        return self.serverType.get()

    def set_selected_server(self, server):
        self.serverType.set(server)

    def get_selected_country(self):
        return self.country.get()

    def set_selected_country(self, country):
        self.country.set(country)
        self.country_menu_button.config(textvariable=self.country)


