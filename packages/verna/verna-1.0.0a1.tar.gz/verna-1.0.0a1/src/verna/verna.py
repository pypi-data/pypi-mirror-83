"""
Data structures used to handle colors in Verna
"""

from typing import Tuple
import colorsys

from verna import names


def _rounded_float(val: float) -> float:
    """
    Similar to the built-in round() except that rounding is done
    towards higher value if val is equally close to the nearest values.
    Like:

    >>> _rounded_float(1.5)  # 2
    >>> _rounded_float(2.5)  # 3
    >>> _rounded_float(3.5)  # 4
    >>> _rounded_float(4.4)  # 4
    >>> _rounded_float(5.6)  # 6

    Built-in round() rounds towards an even value if val is equally close
    to both the nearest values as shown below
    >>> round(1.5)  # 2
    >>> round(2.5)  # 2
    >>> round(3.5)  # 4

    Returns int if val doesn't have decimal place values otherwise value
    returned is a float.
    """
    val_str = str(val)
    if ('.' in val_str) and (val_str[-1] == '5'):
        ndigits = len(val_str) - (val_str.find('.') + 1)
        val_str = val_str[:-1] + '6'
        return round(float(val_str), ndigits)
    return val


def _rounded_int(val: float) -> int:
    """
    Accept a float value, round it upwards with _rounded_float() and return the
    resultant value as an int.
    """
    return round(_rounded_float(val * 0xff))


class Color:
    """
    Represents a color.

    Only RGB scheme is supported.
    """
    def __init__(self, integer: int):
        if integer < 0 or integer > 0xffffffff:
            raise ValueError
        self.integer = integer

    def __int__(self):
        return self.integer

    def __index__(self):
        # for hex()
        return self.integer

    def __repr__(self):
        return f"<Color(0x{self.integer:x})>"

    def __str__(self):
        """
        Returns integer color value in hex form as a string with out any prefix
        """
        return f"{self.integer:x}"

    def __lt__(self, other: object):
        if isinstance(other, Color):
            return self.integer < other.integer
        return NotImplemented

    def __le__(self, other: object):
        if isinstance(other, Color):
            return self.integer <= other.integer
        return NotImplemented

    def __eq__(self, other: object):
        if isinstance(other, Color):
            return self.integer == other.integer
        return NotImplemented

    def __ne__(self, other: object):
        if isinstance(other, Color):
            return self.integer != other.integer
        return NotImplemented

    def __gt__(self, other: object):
        if isinstance(other, Color):
            return self.integer > other.integer
        return NotImplemented

    def __ge__(self, other: object):
        if isinstance(other, Color):
            return self.integer >= other.integer
        return NotImplemented

    def replace(self,
                red: float = None,
                green: float = None,
                blue: float = None,
                alpha: float = None) -> 'Color':
        """
        Returns a new Color by changing properties of a pre-existing instance.
        """
        if red is None:
            red_int = self.red
        else:
            red_int = _rounded_int(self._normalize(red))

        if green is None:
            green_int = self.green
        else:
            green_int = _rounded_int(self._normalize(green))

        if blue is None:
            blue_int = self.blue
        else:
            blue_int = _rounded_int(self._normalize(blue))

        if alpha is None:
            alpha_int = self.alpha
        else:
            alpha_int = _rounded_int(self._normalize(alpha))

        return self.__class__.from_rgba(red_int, green_int,
                                        blue_int, alpha_int)

    def rgba(self) -> Tuple[int, int, int, float]:
        """
        Returns red, green, blue, alpha as a tuple in that order
        """
        return self.red, self.green, self.blue, self.alpha

#    def hsla(self) -> Tuple[int, int, int, float]:
#        """
#        Returns hue, saturation, lightness, alpha as a tuple in that order
#        """
        

    @classmethod
    def from_name(cls, name: str) -> 'Color':
        """
        Returns a Color object based on the given color name.

        Only CSS3 extended color keyword names are supported.
        """
        name = name.lower()
        return cls(names.COLORS[name])

    @classmethod
    def from_rgba(cls,
                  red: float,
                  green: float,
                  blue: float,
                  alpha: float = 0) -> 'Color':
        """
        Returns a Color object from a set of RGBA values
        """
        red_int = _rounded_int(cls._normalize(red))
        green_int = _rounded_int(cls._normalize(green))
        blue_int = _rounded_int(cls._normalize(blue))
        alpha_int = _rounded_int(cls._normalize(alpha))
        integer = ((alpha_int << 24) | (red_int << 16)
                   | (green_int << 8) | blue_int)
        return cls(integer)

    @classmethod
    def to_float(cls, val: float) -> float:
        """
        Returns equivalent float ranging from 0.0 to 1.0 from
        an int ranging from 0 to 255 (eg: 255 -> 1.0)
        Value of val is returned unchanged if it is a float from 0.0 to 1.0

        Raises ValueError if conversion cannot be performed.
        """
        val_float = cls._normalize(val)
        return _rounded_float(val_float)

    @classmethod
    def to_int(cls, val: float) -> int:
        """
        Returns equivalent int ranging from 0 to 255 from:
         - a float ranging from 0 to 1.0 (eg: 0.5 -> 128)
        Value of val is returned unchanged if it is an integer from 0 to 255.

        Raises ValueError if conversion cannot be performed.
        """
        val_float = cls._normalize(val)
        return _rounded_int(val_float)

    @staticmethod
    def _normalize(val: float) -> float:
                   #conv: dict) -> float:
        """
        conv = {str(type): (low, high)}
        OR
        from: str in [float, degree, int]
        #XXX: add a to_degrees() classmethod

        float -> int    (rgb)
        float -> float  (rgba,h)
        degree -> float (h)
        
        """
                                            # possible targets: RGB,Y = [0,1]
                                            #                   H     = [0, 360 deg)
                                            #                   SL    = [0, 100 %] 
                                            #                   I     = [-0.5957, 0.5957]
                                            #                   Q     = [-0.5226, 0.5226]
        """
        Validate and convert a color component value in the form of an
        integer ranging from 0 to 255 or a float ranging from 0.0 to 1.0
        to an equivalent float ranging from 0.0 to 1.0

        val may be an int or a float.

        Raises ValueError if conversion cannot be done.

        Note: Property getter-setters of the class rely on this function.
        """

        if isinstance(val, int) and not isinstance(val, bool):
            # For int, value should be between 0 and 255 (inclusive)
            if val < 0 or val > 255:
                raise ValueError("{val}: Invalid value")
            float_val = val / 0xff

        elif isinstance(val, float):
            # For float, value should be between 0.0 and 1.0 (inclusive)
            if val < 0 or val > 1:
                raise ValueError(f"{val}: Invalid value")
            float_val = val
        else:
            raise ValueError(f"{val}: Invalid value type")

        return float_val

    @property
    def alpha(self) -> float:
        """
        Alpha value ranges from 0 to 1.0
        """
        return (self.integer >> 24) / 0xff

    @alpha.setter
    def alpha(self, val: float):
        val_int = _rounded_int(self._normalize(val))
        self.integer = (val_int << 24) | (self.integer & 0x00ffffff)

    @property
    def red(self) -> int:
        """
        Red value ranges from 0 to 255
        """
        return (self.integer >> 16) & 0xff

    @red.setter
    def red(self, val: float):
        val_int = _rounded_int(self._normalize(val))
        self.integer = (val_int << 16) | (self.integer & 0xff00ffff)

    @property
    def green(self) -> int:
        """
        Grren value ranges from 0 to 255
        """
        return (self.integer >> 8) & 0xff

    @green.setter
    def green(self, val: float):
        val_int = _rounded_int(self._normalize(val))
        self.integer = (val_int << 8) | (self.integer & 0xffff00ff)

    @property
    def blue(self) -> int:
        """
        Blue value ranges from 0 to 255
        """
        return self.integer & 0xff

    @blue.setter
    def blue(self, val: float):
        val_int = _rounded_int(self._normalize(val))
        self.integer = val_int | (self.integer & 0xffffff00)
