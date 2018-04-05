import hashlib
from bytestring_splitter import BytestringSplitter
from copy import deepcopy

_digest_length = 8


class _Constant:
    __repr_content = None
    __bool_repr = None

    def __init__(self, name):
        # Names must be upper case except that dunder names can be set.
        # They're used by a lot of IDE tooling, so let's not mess up a good thing.
        if not name.isupper():
            if not (name.startswith("__") and name.endswith("__")):
                raise ValueError(
                    "Use ALL_CAPS names for constants.  See https://www.python.org/dev/peps/pep-0008/#constants.")
        self.__name = name

    def __setattr__(self, key, value):
        if key in ("_Constant__repr_content", "_Constant__bool_repr", "_Constant__name"):
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

    def __eq__(self, other):
        for_comparison_sake = self._cast_to_other_object_type_or_bytes(other)
        return for_comparison_sake == other

    def __call__(self, representation):
        return self.represent_as(representation)

    def __index__(self):
        return int(self)

    def __len__(self):
        if self.__repr_content is not None:
            return len(self.__repr_content)
        else:
            return len(self.__name)

    def _cast_to_other_object_type_or_bytes(self, other):
        if type(other) in (bytes, int, str):
            # Cast to other object type if it's bytes, int, or str.
            caster = type(other)
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
            self.represent_as(hashlib.sha512(self._Constant__name.encode()).digest()[:_digest_length])

        return caster(self.__repr_content, *args, **kwargs)

    def represent_as(self, representation):
        if self.__repr_content is not None and self.__repr_content is not representation:
            raise ValueError(
                "Can't set representation to a different value once set - it was already set to {} when you tried to set it to {}".format(
                    self.__repr_content, representation))
        elif self.__repr_content is representation:
            return self
        else:
            self.__repr_content = deepcopy(representation)
        return self

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


class __ConstantFactory:

    def __init__(self):
        self.registry = {}

    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            constant = self.registry.setdefault(item.upper(), _Constant(item))
            return constant


constants = __ConstantFactory()
default_constant_splitter = key_splitter = BytestringSplitter((bytes, _digest_length))
