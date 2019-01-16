#!/usr/bin/python3

from bin.gui_components.root_password_window import RootPermissionWindow
from bin.gui import *

def main():
    # if file is launched without root privileges
    if os.geteuid() != 0:
        root_request_win = RootPermissionWindow()
        root_request_win.mainloop()
        # checking if a correct password has been inserted
        from bin.gui_components.root_password_window import password_inserted

        if password_inserted is None:
            return

        import subprocess, bin.root
        bin.root.get_root_permissions(password_inserted)

        import sys
        nordpy_args = ['sudo', 'python3',  *sys.argv]
        subprocess.call(nordpy_args)
    else:
        app = gui()
        app.mainloop()


if __name__ == "__main__":
    main()
