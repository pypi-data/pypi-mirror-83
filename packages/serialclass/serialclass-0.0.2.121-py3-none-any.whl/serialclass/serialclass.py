""" BaseClass entry point - imported by __init__.py

Copyright (c) 2020 Greg Van Aken
"""

import re
import json


class SerialClass:
    """A base class that enables serialized representation of Python classes"""

    def class_attr(self, attr, ignore_protected):
        """Make sure it is just an attribute and not a method, magic or otherwise"""
        protected = False if not ignore_protected else self.protected_attr(attr)
        return re.match('^(?!__).*', attr) and not callable(getattr(self, attr)) and not protected

    def serialize(self, *args, **kwargs):  # pylint: disable = unused-argument
        """Get the serialized representation as a dict"""
        attribs = {}
        depth = kwargs.get('depth', float('inf'))
        calls = kwargs.get('calls', 0)
        ignore_protected = kwargs.get('ignore_protected', False)
        for attr in dir(self):
            if self.class_attr(attr, ignore_protected):
                attribs[attr] = self.unpack(getattr(self, attr), depth=depth,
                                            calls=calls, ignore_protected=ignore_protected)
        return {type(self).__name__: attribs}

    def stringify(self, *args, **kwargs):
        """Get a jsonstring from the dict representation of the class"""
        return json.dumps(self.serialize(*args, **kwargs), default=SerialClass.string_repr)

    def pstringify(self, *args, **kwargs):
        """Get a pretty jsonstring from the dict representation of the class"""
        return json.dumps(self.serialize(*args, **kwargs), indent=4,
                          sort_keys=True, default=SerialClass.string_repr)

    # --Static Methods-- #
    @staticmethod
    def unpack(elem, depth=float('inf'), calls=0, ignore_protected=False):
        """Given an attribute value, make it a dict if possible"""
        if calls < depth:
            try:
                return elem.serialize(depth=depth, calls=calls + 1,
                                      ignore_protected=ignore_protected)
            except AttributeError:
                if isinstance(elem, list):
                    return [SerialClass.unpack(item, depth=depth, calls=calls + 1,
                                               ignore_protected=ignore_protected) for item in elem]
                if isinstance(elem, dict):
                    return {SerialClass.unpack(
                        k, depth=depth, calls=calls + 1,
                        ignore_protected=ignore_protected):
                                SerialClass.unpack(elem[k],
                                                   depth=depth, calls=calls + 1) for k in elem}
        return elem

    @staticmethod
    def string_repr(obj):
        """Just get the class name + object"""
        return str(obj).split(' at ')[0] + '>'

    @staticmethod
    def protected_attr(attr):
        """Primitive, but check to see if it startswith _"""
        return attr.startswith('_')
