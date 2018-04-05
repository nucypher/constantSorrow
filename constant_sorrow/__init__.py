from bytestring_splitter import BytestringSplitter
_digest_length = 8

default_constant_splitter = key_splitter = BytestringSplitter((bytes, _digest_length))