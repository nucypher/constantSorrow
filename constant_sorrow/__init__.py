from constant_sorrow.__about__ import __author__, __summary__, __title__, __version__
__all__ = ["__title__", "__summary__", "__version__", "__author__", ]


from bytestring_splitter import BytestringSplitter
_digest_length = 8

default_constant_splitter = key_splitter = BytestringSplitter((bytes, _digest_length))


def constant_or_bytes(possible_constant):
    from .constants import _Constant
    from .constants import _constants_registry_by_hash
    """
    Utility function for getting a constant (that has already been registered) from a serialized constant (ie, bytes of its hash)
    """
    if _Constant in possible_constant.__class__.__bases__:
        result = possible_constant
    else:
        bytes_of_possible_constant = bytes(possible_constant)
        try:
            constant = _constants_registry_by_hash[bytes_of_possible_constant]
            result = constant
        except KeyError:
            result = bytes_of_possible_constant
    return result