from constant_sorrow.__about__ import __author__, __summary__, __title__, __version__
__all__ = ["__title__", "__summary__", "__version__", "__author__", ]


from bytestring_splitter import BytestringSplitter
_digest_length = 8

default_constant_splitter = key_splitter = BytestringSplitter((bytes, _digest_length))