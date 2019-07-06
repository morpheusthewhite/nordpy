#!/usr/bin/python3

from bin.gui_components.root_password_window import RootPermissionWindow
import os


def main():
    # if file is launched without root privileges
    if os.geteuid() != 0:
        root_request_win = RootPermissionWindow()
        root_request_win.mainloop()
        # checking if a correct password has been inserted
        from bin.gui_components.root_password_window import password_inserted

        if password_inserted is None:
            return

        import bin.root
        bin.root.get_root_permissions(password_inserted)
        del password_inserted

        from bin.gui import gui
        app = gui()
        app.mainloop()


if __name__ == "__main__":
    main()
