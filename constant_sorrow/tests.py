import pytest


def test_different_constants_are_unequal():
    from constant_sorrow import constants
    assert constants.ONE_THING != constants.ANOTHER_THING


def test_same_constants_are_equal():
    from constant_sorrow import constants
    assert constants.SAME_THING is constants.SAME_THING


def test_bytes_representation():
    """
    A constant can be represented as some specific bytes.
    """
    from constant_sorrow import constants
    llamas = constants.LLAMAS
    bytes_repr = b"llamas_as_bytes"
    constants.LLAMAS.represent_as(bytes_repr)
    assert bytes(llamas) == bytes_repr


def test_bytes_representation_default():
    from constant_sorrow import constants
    another_constant = constants.ANOTHER_CONSTANT
    assert len(bytes(another_constant)) == 8
    assert bytes(another_constant) == constants.ANOTHER_CONSTANT


def test_cant_represent_as_bytes_again():
    from constant_sorrow import constants

    # Here's a shortcut for setting the representation.
    constants.DINGOS("a certain dingo")

    # We can't change the value once it is set.
    with pytest.raises(ValueError):
        constants.DINGOS("something else")

    # However setting the same value again is permitted.
    constants.DINGOS("a certain dingo")


def test_cast_representation():
    from constant_sorrow import constants
    bytes_repr = b"14"
    constants.FOURTEEN.represent_as(bytes_repr)

    assert int(constants.FOURTEEN) == 14
    assert bytes(constants.FOURTEEN) == b"14"
    assert str(constants.FOURTEEN) == "14"
