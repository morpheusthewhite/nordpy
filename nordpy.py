#!/usr/bin/python3

from bin.gui import gui
from bin.gui_components.root_password_window import RootWindow, password_inserted

def main():
    root_request_win = RootWindow()
    root_request_win.mainloop()

    # checking if a correct password has been inserted
    from bin.gui_components.root_password_window import password_inserted
    if password_inserted is not None:
        app = gui()
        app.mainloop()


if __name__ == "__main__":
    main()
