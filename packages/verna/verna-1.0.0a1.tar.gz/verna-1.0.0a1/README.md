<h1> Verna </h1>

<a href="https://pypi.org/project/verna"><img alt="PyPI" src="https://img.shields.io/pypi/v/verna"></a>
<img alt="Build Status" src="https://api.travis-ci.com/ju-sh/verna.svg?branch=master"></img>
<a href="https://github.com/ju-sh/verna/blob/master/LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/pypi/l/verna"></a>

A simple module to handle colors

Only [RGBA colors](https://en.wikipedia.org/wiki/RGBA_color_model) are supported at the moment.

---

<h2>Installation</h2>

You need Python>=3.6 to use Verna.

It can be installed from PyPI with pip using

    pip install verna

---

<h2>Usage</h2>

Colors are represented using objects of class `Color`. 

The color value is essentially stored as an integer as the `integer` attribute.

Alpha channel value can be set to denote opacity level.

The following properties can be used to access the different color components.

    color.alpha
    color.red
    color.green
    color.blue

where `color` is an instance of `Color`.

The different color components can be edited with one of the following values

 - an integer from 0 to 255 (eg: 0xff, 255)
 - a float from 0.0 to 1.0 (eg: 0.4)

A value outside of valid range would cause exception.

So, the following are valid:

    color = Color(0x00ffff)
    color.alpha = 0x80
    color.alpha = 0.5 
    color.red = 0xff        # Same as color.red = 255
    color.green = 217
    color.blue = 0xf5
    color.blue = 0.75

whereas the following will cause error:

    color = Color(0x00ffff)
    color.alpha = 0x1ff    # > 0xff
    color.alpha = -1       # < 0.0
    color.alpha = 1.2      # > 1.0
    color.alpha = True     # Invalid type: bool


<h4>Color component value conversions</h4>

Following functions can be used for basic inter-conversion for the color
component values:

    > Color.to_int()

Example:

    >>> color = Color.from_name("red")      # 0xff0000
    >>> red_int = Color.to_int(color.red)   # 255

Convert a float in the range of 0.0 till 1.0 towards an int in the range
of 0 to 255.

    > Color.to_float()

Example:

    >>> color = Color.from_name("darkolivegreen")   # 0x556b2f
    >>> red_float = Color.to_float(color.red)       # 0.1843137254901961

Convert an int in the range of 0 till 255 towards a float in the range
of 0 to 0.1

**Conversion to percentage values** can be done by multiplying the float
value obtained with `Color.to_float()` by 100.

    >>> float_val = Color.to_float(54)  # 0.21176470588235294
    >>> percentage = float_val * 100    # 21.176470588235294

<h4>Creating `Color` object</h4>

A `Color` object may be created in multiple ways.

<h5>From integer color code</h5>

For example, cyan (solid), which has color code `0x00ffff` can be created like

    Color(0x00ffff)

which is same as

    Color(65535)

<h5>From color name</h5>

`Color.from_name()` can be used to create `Color` objects from a [CSS3 color name](https://www.w3.org/wiki/CSS3/Color/Extended_color_keywords).

For example, cyan can be created with

    Color.from_name('cyan')

<h5>From RGBA values</h5>

`Color.from_rgba()` can be used to create an instance of `Color` from RGBA values.

    Color.from_rgba(255, 255, 0)         # solid yellow
    Color.from_rgba(255, 255, 0, 0.5)    # translucent yellow


<h4>Other methods</h4>

> Color.replace(red, green, blue, alpha)

Create a new `Color` object by replacing some of the component values
of a `Color` object.

Example:

    >>> color = Color(0x8000ffff)
    >>> color.replace(red=0x80, green=59, blue=0.5)   # color with hex value 0x80803b80

> Color.rgba()

Returns the color component values of `red`, `green`, `blue`, `alpha` as a tuple.

Example:

    >>> color = Color(0x8000ffff)
    >>> color.rgba()
    (0, 255, 255, 0.5)

> hex()

Return hexcode of the color value in ARGB format as a string.

Example:

    >>> color = Color(0x8000ffff)
    >>> hex(color)
    0x8000ffff

> int()

Return color of the color value in ARGB format as an integer.

Example:

    >>> color = Color(0x8000ffff)
    >>> int(color)
    2147549183

