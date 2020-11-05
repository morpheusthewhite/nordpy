from tkinter import *
from bin.font_size import get_font_scale_factor
use_si = True
try:
    import screeninfo
except ImportError:
    use_si = False


DEFAULT_SCALE_FACTOR = 1


def get_monitor_from_coord(x, y):
    """
    Return monitor for the monitor

    Args:
        x: (todo): write your description
        y: (todo): write your description
    """
    monitors = screeninfo.get_monitors()

    for m in reversed(monitors):
        if m.x <= x <= m.width + m.x and m.y <= y <= m.height + m.y:
            return m
    return monitors[0]


class CenteredWindow(Tk):
    """
    A Tk class for exposing a centering and scaling function
    """
    def center_window(self, width=300, height=200, scale=DEFAULT_SCALE_FACTOR, font_name='TkDefaultFont'):
        """
        Center the main window.

        Args:
            self: (todo): write your description
            width: (int): write your description
            height: (todo): write your description
            scale: (float): write your description
            DEFAULT_SCALE_FACTOR: (float): write your description
            font_name: (str): write your description
        """
        # gets screen width and height
        if use_si:
            # Get the screen which contains this window
            current_screen = get_monitor_from_coord(self.winfo_pointerx(), self.winfo_pointery())

            screen_width = current_screen.width
            screen_height = current_screen.height
            offset_x = current_screen.x
            offset_y = current_screen.y
        else:
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            offset_x = 0
            offset_y = 0

        font_factor = get_font_scale_factor(font_name)

        scaled_width = width * scale * font_factor
        scaled_height = height * scale * font_factor

        # calculates position x and y coordinates
        x = offset_x + (screen_width / 2) - (scaled_width / 2)
        y = offset_y + (screen_height / 2) - (scaled_height / 2)
        self.geometry('%dx%d+%d+%d' % (scaled_width, scaled_height, x, y))


class CenteredTopLevel(Toplevel):
    """
    A TopLevel class for exposing a centering and scaling function
    """
    def center_window(self, width=300, height=200, scale=DEFAULT_SCALE_FACTOR, font_name='TkDefaultFont'):
        """
        Center the main window.

        Args:
            self: (todo): write your description
            width: (int): write your description
            height: (todo): write your description
            scale: (float): write your description
            DEFAULT_SCALE_FACTOR: (float): write your description
            font_name: (str): write your description
        """
        # gets screen width and height
        if use_si:
            # Get the screen which contains this window
            current_screen = get_monitor_from_coord(self.winfo_pointerx(), self.winfo_pointery())

            screen_width = current_screen.width
            screen_height = current_screen.height
            offset_x = current_screen.x
            offset_y = current_screen.y
        else:
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            offset_x = 0
            offset_y = 0

        font_factor = get_font_scale_factor(font_name)

        scaled_width = width * scale * font_factor
        scaled_height = height * scale * font_factor

        # calculates position x and y coordinates
        x = offset_x + (screen_width / 2) - (scaled_width / 2)
        y = offset_y + (screen_height / 2) - (scaled_height / 2)
        self.geometry('%dx%d+%d+%d' % (scaled_width, scaled_height, x, y))