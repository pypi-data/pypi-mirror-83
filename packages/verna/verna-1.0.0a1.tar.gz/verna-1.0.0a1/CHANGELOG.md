<h4> v1.0.0 () </h4>

 - Disallow percentage values as strings. Float value can readily be
   converted to percentage.
 - Allow assigning float values (ranging from 0.0 to 1.0) for red,
   green and blue properties.
 - Add `to_int()`, `to_float()` and `to_percentage()` functions.
 - Color is no longer a sub-class of `int`.
 - Color.__repr__() shows value in hexadecimal now.

<h4> v0.0.2 (16 Oct 2020) </h4>

 - Fix error in `Color.from_name()` so that it returns `Color` instead of `int`.
 - Use setuptools for packaging.

<h4> v0.0.1 (15 Oct 2020) </h4>

First version
