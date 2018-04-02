import hashlib
from bytestring_splitter import BytestringSplitter

_digest_length = 8


class _Constant:
    _repr_content = None

    def __init__(self, name):
        self.name = name

    def __setattr__(self, key, value):
        if key in ("_repr_content", "name"):
            super().__setattr__(key, value)
        else:
            raise TypeError("Don't try to set values on a constant.  I mean, what's the point?")

    def __bytes__(self):
        return self._cast_repr(bytes)

    def __int__(self):
        return self._cast_repr(int)

    def __str__(self):
        return self._cast_repr(str, encoding="utf-8")

    def __repr__(self):
        return "Constant: {}".format(self.name)

    def __add__(self, other):
        return self._cast_to_other_object_type_or_bytes(other) + other

    def __radd__(self, other):
        return other + self._cast_to_other_object_type_or_bytes(other)

    def __eq__(self, other):
        for_comparison_sake = self._cast_to_other_object_type_or_bytes(other)
        return for_comparison_sake == other

    def __call__(self, representation):
        return self.represent_as(representation)

    def _cast_to_other_object_type_or_bytes(self, other):
        if type(other) in (bytes, int, str):
            # Cast to other object type if it's bytes, int, or str.
            caster = type(other)
        else:
            # bytes otherwise.
            caster = bytes
        return caster(self)

    def _cast_repr(self, caster, *args, **kwargs):
        """
        Will cast this constant with the provided caster, passing args and kwargs.

        If there is no registered representation, will hash the name using sha512 and use the first 8 bytes
        of the digest.
        """
        if self._repr_content is None:
            self.represent_as(hashlib.sha512(self.name.encode()).digest()[:_digest_length])
        try:
            return caster(self._repr_content, *args, **kwargs)
        except AttributeError:
            raise TypeError("This constant doesn't have representation content.")

    def represent_as(self, representation):
        if self._repr_content is not None and self._repr_content is not representation:
            raise ValueError("Can't set representation to a different value once set - it was already set to {} when you tried to set it to {}".format(self._repr_content, representation))
        elif self._repr_content is representation:
            return
        else:
            self._repr_content = representation
        return self


class __ConstantFactory:

    def __init__(self):
        self.registry = {}

    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            constant = self.registry.setdefault(item.upper(), _Constant(item.upper()))
            return constant


constants = __ConstantFactory()
default_constant_splitter = key_splitter = BytestringSplitter((bytes, _digest_length))
