from tkinter import font

FONT_DEFAULT_SIZE = 9
FONT_DEFAULT_SIZE_PIXEL = -12

def get_font_scale_factor(font_name):
    """
    Calculate the ratio between the system font and the default font, on which default sizes are based
    :return the ratio between system font (currently used) and the default font 
    """
    font_size_system = font.nametofont(font_name).cget("size")
    
    if font_size_system > 0:
        # pt size
        return font_size_system / FONT_DEFAULT_SIZE
    else:
        return font_size_system / FONT_DEFAULT_SIZE_PIXEL

