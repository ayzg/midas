import math

NoteNameT = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

class TRect:
    def __init__(self, left, top, right, bottom):
        """
        Initializes a rectangle with the given coordinates.

        Parameters:
        - left (int): Left coordinate of the rectangle.
        - top (int): Top coordinate of the rectangle.
        - right (int): Right coordinate of the rectangle.
        - bottom (int): Bottom coordinate of the rectangle.
        """
        self.Top = top
        self.Left = left
        self.Bottom = bottom
        self.Right = right

    def Width(self):
        """
        Calculates the width of the rectangle.

        Returns:
        - int: Width of the rectangle.
        """
        return self.Right - self.Left

    def Height(self):
        """
        Calculates the height of the rectangle.

        Returns:
        - int: Height of the rectangle.
        """
        return self.Bottom - self.Top

class TClipLauncherLastClip:
    def __init__(self, track_num, sub_num, flags):
        """
        Initializes a TClipLauncherLastClip object.

        Parameters:
        - track_num (int): Track number.
        - sub_num (int): Sub-number.
        - flags (int): Flags for the last clip.
        """
        self.TrackNum = track_num
        self.SubNum = sub_num
        self.Flags = flags

def rect_overlap_equal(rect1, rect2):
    """
    Checks if two rectangles overlap exactly.

    Parameters:
    - rect1 (TRect): First rectangle.
    - rect2 (TRect): Second rectangle.

    Returns:
    - bool: True if rectangles overlap exactly, False otherwise.
    """
    return (rect1.Left <= rect2.Right) & (rect1.Right >= rect2.Left) & (rect1.Top <= rect2.Bottom) & (rect1.Bottom >= rect2.Top)

def rect_overlap(rect1, rect2):
    """
    Checks if two rectangles overlap.

    Parameters:
    - rect1 (TRect): First rectangle.
    - rect2 (TRect): Second rectangle.

    Returns:
    - bool: True if rectangles overlap, False otherwise.
    """
    return (rect1.Left < rect2.Right) & (rect1.Right > rect2.Left) & (rect1.Top < rect2.Bottom) & (rect1.Bottom > rect2.Top)

def limited(value, minimum, maximum):
    """
    Limits a value to a specified range.

    Parameters:
    - value (float): The value to be limited.
    - minimum (float): Minimum allowed value.
    - maximum (float): Maximum allowed value.

    Returns:
    - float: The limited value.
    """
    if value <= minimum:
        result = minimum
    else:
        result = value
    if result > maximum:
        result = maximum
    return result

def inter_no_swap(x, a, b):
    """
    Checks if a value is within a specified range without swapping.

    Parameters:
    - x (float): The value to be checked.
    - a (float): Lower bound of the range.
    - b (float): Upper bound of the range.

    Returns:
    - bool: True if x is in the range [a, b], False otherwise.
    """
    return (x >= a) & (x <= b)

def div_mod_u(a, b):
    """
    Divides two numbers and returns the quotient and remainder.

    Parameters:
    - a (int): Dividend.
    - b (int): Divisor.

    Returns:
    - tuple: Quotient and remainder.
    """
    c = a % b
    return (a // b), c

def swap_int(a, b):
    """
    Swaps the values of two integers.

    Parameters:
    - a (int): First integer.
    - b (int): Second integer.

    Returns:
    - tuple: The swapped values (b, a).
    """
    return b, a

def zeros(value, n_chars, c='0'):
    """
    Converts an integer to a zero-padded string with a specified length.

    Parameters:
    - value (int): The integer value to be converted.
    - n_chars (int): The length of the resulting string.
    - c (str): The padding character (default is '0').

    Returns:
    - str: The zero-padded string.
    """
    if value < 0:
        result = str(-value)
        result = '-' + c * (n_chars - len(result)) + result
    else:
        result = str(value)
        result = c * (n_chars - len(result)) + result
    return result

def zeros_strict(value, n_chars, c='0'):
    """
    Converts an integer to a zero-padded string with a specified length, strict version.

    Parameters:
    - value (int): The integer value to be converted.
    - n_chars (int): The length of the resulting string.
    - c (str): The padding character (default is '0').

    Returns:
    - str: The zero-padded string (truncated if necessary).
    """
    result = zeros(value, n_chars, c)
    if len(result) > n_chars:
        result = result[len(result) - n_chars:]
    return result

def sign(value):
    """
    Returns the sign of a number.

    Parameters:
    - value (float): The input number.

    Returns:
    - int: The sign of the input (-1 for negative, 0 for zero, 1 for positive).
    """
    if value < 0:
        return -1
    elif value == 0:
        return 0
    else:
        return 1

def sign_of(value):
    """
    Returns the sign of a number.

    Parameters:
    - value (float): The input number.

    Returns:
    - int: The sign of the input (-1 for negative, 0 for zero, 1 for positive).
    """
    if value == 0:
        return 0
    elif value < 0:
        return -1
    else:
        return 1

def knob_accel_to_res2(value):
    """
    Converts a knob acceleration value to a resolution value.

    Parameters:
    - value (float): The knob acceleration value.

    Returns:
    - float: The corresponding resolution value.
    """
    n = abs(value)
    if n > 1:
        res = n ** 0.75
    else:
        res = 1
    return res

def offset_rect(rect, dx, dy):
    """
    Offsets the coordinates of a rectangle.

    Parameters:
    - rect (TRect): The rectangle to be offset.
    - dx (int): The horizontal offset.
    - dy (int): The vertical offset.
    """
    rect.Left = rect.Left + dx
    rect.Top = rect.Top + dy
    rect.Right = rect.Right + dx
    rect.Bottom = rect.Bottom + dy

def rgb_to_hsv(r, g, b):
    """
    Converts RGB color values to HSV.

    Parameters:
    - r (float): Red component (in the range [0, 1]).
    - g (float): Green component (in the range [0, 1]).
    - b (float): Blue component (in the range [0, 1]).

    Returns:
    - tuple: HSV values (Hue, Saturation, Value).
    """
    Min = min(min(r, g), b)
    V = max(max(r, g), b)

    Delta = V - Min

    if V == 0:
        S = 0
    else:
        S = Delta / V

    if S == 0.0:
        H = 0.0 
    else:
        if r == V:
            H = 60.0 * (g - b) / Delta
        elif g == V:
            H = 120.0 + 60.0 * (b - r) / Delta
        elif b == V:
            H = 240.0 + 60.0 * (r - g) / Delta

        if H < 0.0:
            H = H + 360.0

    return H, S, V

def rgb_to_hsv_color(color):
    """
    Converts an RGB color value to HSV.

    Parameters:
    - color (int): RGB color value.

    Returns:
    - tuple: HSV values (Hue, Saturation, Value).
    """
    r = ((color & 0xFF0000) >> 16) / 255
    g = ((color & 0x00FF00) >> 8) / 255
    b = ((color & 0x0000FF) >> 0) / 255
    H, S, V = rgb_to_hsv(r, g, b)
    return H, S, V

def hsv_to_rgb(h, s, v):
    """
    Converts HSV color values to RGB.

    Parameters:
    - h (float): Hue component (in degrees).
    - s (float): Saturation component (in the range [0, 1]).
    - v (float): Value component (in the range [0, 1]).

    Returns:
    - tuple: RGB color values (Red, Green, Blue).
    """
    h_temp = 0
    if s == 0.0:
        R = v
        G = v
        B = v
    else:
        if h == 360.0:
            h_temp = 0.0
        else:
            h_temp = h

        h_temp = h_temp / 60
        i = math.trunc(h_temp)
        f = h_temp - i

        p = v * (1.0 - s)
        q = v * (1.0 - (s * f))
        t = v * (1.0 - (s * (1.0 - f)))

        if i == 0:
            R = v
            G = t
            B = p
        elif i == 1:
            R = q
            G = v
            B = p
        elif i == 2:
            R = p
            G = v
            B = t
        elif i == 3:
            R = p
            G = q
            B = v
        elif i == 4:
            R = t
            G = p
            B = v
        elif i == 5:
            R = v
            G = p
            B = q
    return R, G, B

def get_note_name(note_num):
    """
    Gets the musical note name for a MIDI note number.

    Parameters:
    - note_num (int): MIDI note number.

    Returns:
    - str: Musical note name.
    """
    note_num += 1200
    return NoteNameT[note_num % 12] + str((note_num // 12) - 100)

def color_to_rgb(color):
    """
    Converts an RGB color value to its individual components.

    Parameters:
    - color (int): RGB color value.

    Returns:
    - tuple: RGB components (Red, Green, Blue).
    """
    return (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF

def rgb_to_color(r, g, b):
    """
    Converts RGB components to an RGB color value.

    Parameters:
    - r (int): Red component.
    - g (int): Green component.
    - b (int): Blue component.

    Returns:
    - int: RGB color value.
    """
    return (r << 16) | (g << 8) | b

def fade_color(start_color, end_color, value):
    """
    Fades a color between two given colors.

    Parameters:
    - start_color (int): Starting RGB color value.
    - end_color (int): Ending RGB color value.
    - value (int): Fade value (in the range [0, 255]).

    Returns:
    - int: Faded RGB color value.
    """
    r_start, g_start, b_start = color_to_rgb(start_color)
    r_end, g_end, b_end = color_to_rgb(end_color)
    ratio = value / 255
    r_end = round(r_start * (1 - ratio) + (r_end * ratio))
    g_end = round(g_start * (1 - ratio) + (g_end * ratio))
    b_end = round(b_start * (1 - ratio) + (b_end * ratio))
    return rgb_to_color(r_end, g_end, b_end)

def lighten_color(color, value):
    """
    Lightens a color by a specified value.

    Parameters:
    - color (int): RGB color value.
    - value (int): Lightening value (in the range [0, 255]).

    Returns:
    - int: Lightened RGB color value.
    """
    r, g, b = color_to_rgb(color)
    ratio = value / 255
    return rgb_to_color(round(r + (1.0 - r) * ratio), round(g + (1.0 - g) * ratio), round(b + (1.0 - b) * ratio))

def vol_to_db(value):
    """
    Converts a volume value to decibels.

    Parameters:
    - value (float): The volume value.

    Returns:
    - float: The corresponding decibel value.
    """
    value = (math.exp(value * math.log(11)) - 1) * 0.1
    if value == 0:
        return 0
    return round(math.log10(value) * 20, 1)
