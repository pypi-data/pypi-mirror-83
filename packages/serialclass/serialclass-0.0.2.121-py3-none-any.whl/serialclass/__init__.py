""" Library that adds a base class to get a serialized representation of Python classes.

Copyright (c) 2020 Greg Van Aken
"""
from serialclass.serialclass import SerialClass

BUILDNUM = '121'  # on CI builds - this is replaced with auto-incrementing build num
__version__ = f'0.0.2.{BUILDNUM}'
