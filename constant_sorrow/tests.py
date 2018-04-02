import pytest


def test_different_constants_are_unequal():
    from constant_sorrow import constants
    assert constants.ONE_THING != constants.ANOTHER_THING


def test_same_constants_are_equal():
    from constant_sorrow import constants
    assert constants.SAME_THING is constants.SAME_THING


def test_bytes_representation():
    from constant_sorrow import constants
    llamas = constants.LLAMAS
    with pytest.raises(TypeError):
        bytes(llamas)
    bytes_repr = b"llamas_as_bytes"
    constants.LLAMAS.set_representation(bytes_repr)
    assert bytes(llamas) == bytes_repr


def test_cant_represent_as_bytes_again():
    from constant_sorrow import constants
    bytes_repr = b"llamas_as_bytes"
    constants.DINGOS.set_representation(bytes_repr)

    # We can't change the value once it is set.
    with pytest.raises(ValueError):
        constants.DINGOS.set_representation("something else")

    # However setting the same value again is permitted.
    constants.DINGOS.set_representation(bytes_repr)


def test_cast_representation():
    from constant_sorrow import constants
    bytes_repr = b"14"
    constants.FOURTEEN.set_representation(bytes_repr)

    assert int(constants.FOURTEEN) == 14
    assert bytes(constants.FOURTEEN) == b"14"
    assert str(constants.FOURTEEN) == "14"
