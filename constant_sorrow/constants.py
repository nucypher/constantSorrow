import hashlib
import sys
from copy import deepcopy
from types import ModuleType

from . import _digest_length


class _Constant:
    __repr_content = None
    __bool_repr = None
    __uses_default_repr = True
    __has_been_stringified = False

    class OldKentucky(RuntimeError):
        pass

    def __init__(self, name):
        # Names must be upper case except that dunder names can be set.
        # They're used by a lot of IDE tooling, so let's not mess up a good thing.
        if not name.isupper():
            if not (name.startswith("__") and name.endswith("__")):
                raise ValueError(
                    "Use ALL_CAPS names for constants.  See https://www.python.org/dev/peps/pep-0008/#constants.")
        self.__name = name

    def __setattr__(self, key, value):
        if key in ("_Constant__repr_content", "_Constant__bool_repr", "_Constant__name", "_Constant__uses_default_repr",
                   "_Constant__has_been_stringified"):
            super().__setattr__(key, value)
        else:
            raise TypeError("Don't try to set values on a constant.  I mean, what's the point?")

    def __getattr__(self, item):
        try:
            return getattr(self.__repr_content, item)
        except AttributeError:
            raise AttributeError("Without a representation, you can't use {}.".format(item))

    def __bytes__(self):
        if type(self.__repr_content) == str:
            return self._cast_repr(bytes, encoding="utf-8")
        else:
            return self._cast_repr(bytes)

    def __int__(self):
        return self._cast_repr(int)

    def __str__(self):
        # Unless there's an explicit repr, we want the str value to be the name.
        if type(self.__repr_content) is None or self.__uses_default_repr:
            self.__has_been_stringified = True
            return self.__name
        if type(self.__repr_content) == bytes:
            return self._cast_repr(str, encoding="utf-8")
        else:
            return self._cast_repr(str)

    def __bool__(self):
        if self.__bool_repr is None:
            if self.__repr_content is None:
                raise TypeError("This constant can't currently be represented as a bool.")
            else:
                return bool(self.__repr_content)
        else:
            return self.__bool_repr

    def __repr__(self):
        if self.__repr_content is not None:
            return "{} ({})".format(self.__name, self.__repr_content)
        else:
            return self.__name

    def __add__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) + other

    def __radd__(self, other):
        return other + self._cast_to_other_object_type_or_bytes(other)

    def __sub__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) - other

    def __rsub__(self, other):
        return other - self._cast_to_other_object_type_or_bytes(other)

    def __mul__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) * other

    def __rmul__(self, other):
        return other * self._cast_to_other_object_type_or_bytes(other)

    def __truediv__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) / other

    def __rtruediv__(self, other):
        return other / self._cast_to_other_object_type_or_bytes(other)

    def __floordiv__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) // other

    def __rfloordiv__(self, other):
        return other // self._cast_to_other_object_type_or_bytes(other)

    def __gt__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) > other

    def __ge__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) >= other

    def __lt__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) < other

    def __le__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) <= other

    def __eq__(self, other):
        for_comparison_sake = self._cast_to_other_object_type_or_bytes(other)
        return for_comparison_sake == other

    def __call__(self, representation):
        if self.__repr_content is not None and self.__repr_content is not representation:
            message = "Can't set representation to a different value once set - it was " \
                      "already set to {} when you tried to set it to {}"
            raise ValueError(message.format(self.__repr_content, representation))

        if self.__has_been_stringified:
            if not self.__name == str(representation):
                message = "This Constant has already been represented as the string {} and can't be changed to be represented by {}"
                raise ValueError(message.format(self.__name, str(representation)))

        elif self.__repr_content is representation:
            return self
        else:
            self.__uses_default_repr = False
            self.__repr_content = deepcopy(representation)

        return self

    def __index__(self):
        return int(self)

    def __len__(self):
        if self.__repr_content is not None:
            return len(self.__repr_content)
        else:
            return len(self.__name)

    def __iter__(self):
        for item in self.__repr_content:
            yield item

    @property
    def _sorrow_type(self):
        if self.__repr_content is None:
            raise self.OldKentucky
        repr_type = type(self.__repr_content)
        return repr_type

    def _cast_to_other_object_type_or_bytes(self, other):
        if type(other) in (bytes, int, str):
            # Cast to other object type if it's bytes, int, or str.
            caster = type(other)
        elif type(other) is _Constant:
            try:
                caster = other._sorrow_type
            except self.OldKentucky:
                caster = bytes
        else:
            # bytes otherwise.
            caster = bytes
        # if type(other) == bytes and type(self.__repr_content) == str:
        #     return self._cast_repr(str, encoding="utf-8")
        # else:
        return caster(self)

    def _cast_repr(self, caster, *args, **kwargs):
        """
        Will cast this constant with the provided caster, passing args and kwargs.

        If there is no registered representation, will hash the name using sha512 and use the first 8 bytes
        of the digest.
        """
        if self.__repr_content is None:
            self(hashlib.sha512(self._Constant__name.encode()).digest()[:_digest_length])

        return caster(self.__repr_content, *args, **kwargs)

    def bool_value(self, bool_value):
        if self.__repr_content is not None:
            if bool(self) is not bool(bool_value):
                raise ValueError("Based on the set representation, {} was previously {}; can't change to {}.".format(
                    self.__name,
                    bool(self),
                    bool(bool_value)))

        if self.__bool_repr is not None:
            if bool(self) is not bool(bool_value):
                raise ValueError("The specified bool value for {} was previously {}; can't change to {}.".format(
                    self.__name,
                    bool(self),
                    bool(
                        bool_value)))

        self.__bool_repr = bool(bool_value)
        return self


_constants_registry = {}


class __ConstantFactory(ModuleType):

    def __getattr__(self, item):
        constant = _constants_registry.setdefault(item.upper(), _Constant(item))
        return constant


sys.modules[__name__].__class__ = __ConstantFactory
