import pytest
from constant_sorrow import constants


def test_establishing_a_constant():
    # You get a constant by just picking an all-caps name and using it as an attr on constants.
    like_this = constants.THIS_IS_A_VALID_CONSTANT

    # But you can't make a constant in lower case.
    with pytest.raises(ValueError):
        constants.this_is_not_the_right_case_for_a_constant


def test_different_constants_are_unequal():
    assert constants.ONE_THING != constants.ANOTHER_THING


def test_same_constants_are_identical():
    assert constants.SAME_THING == constants.SAME_THING
    assert constants.SAME_THING is constants.SAME_THING


def test_set_representation():
    """A constant can be represented as some specific bytes."""
    llamas = constants.LLAMAS
    constants.LLAMAS.represent_as(b"llamas_as_bytes")
    assert bytes(llamas) == b"llamas_as_bytes"

    # Here's a shortcut for setting the representation.
    constants.AFRICAN_SWALLOW(b"non-migratory")
    assert bytes(constants.AFRICAN_SWALLOW) == b"non-migratory"


def test_bytes_representation_default():
    """By default, constants are represented as a SHA512 hash of their name, truncated to 8 bytes."""
    another_constant = constants.ANOTHER_CONSTANT
    assert len(bytes(another_constant)) == 8
    assert bytes(another_constant) == constants.ANOTHER_CONSTANT


def test_cast_representation():
    bytes_repr = b"14"
    constants.FOURTEEN.represent_as(bytes_repr)

    assert int(constants.FOURTEEN) == 14
    assert bytes(constants.FOURTEEN) == b"14"
    assert str(constants.FOURTEEN) == "14"


def test_cant_change_representation():
    constants.DINGOS("a certain dingo")

    # We can't change the value once it is set.
    with pytest.raises(ValueError):
        constants.DINGOS("something else")

    # However setting the same value again is permitted.
    constants.DINGOS("a certain dingo")

    assert bytes(constants.DINGOS) == b"a certain dingo"


def test_bool_representation():
    # Unlike representing as bytes, you can't automatically represent as bool.
    with pytest.raises(TypeError):
        bool(constants.NO_KNOWN_BOOL)

    # You can either set the representation...
    constants.WITH_BOOL_FROM_REPR("non-empty strings are True, obviously.")
    assert bool(constants.WITH_BOOL_FROM_REPR) is True

    # Or you can specifically set a bool representation.
    constants.WITH_SET_BOOL.bool_value(False)
    assert bool(constants.WITH_SET_BOOL) is False

    # A set boolean value will take precedence over the representation.
    constants.WITH_SET_BOOL("this string is non-empty, but this constant is still False.")
    assert bool(constants.WITH_SET_BOOL) is False

    # You can set it to the value again...
    constants.WITH_BOOL.bool_value(False)

    # But you can't change the bool value once set.
    with pytest.raises(ValueError):
        constants.WITH_BOOL.bool_value(True)

    # Also, we can't take the first constant above and set its bool value to False,
    # because it's a constant and it was already true by dint of its representation.
    with pytest.raises(ValueError):
        constants.WITH_BOOL_FROM_REPR.bool_value(False)

    # We can, however, set it to True, because its current value is True.
    constants.WITH_BOOL_FROM_REPR.bool_value(True)
    assert bool(constants.WITH_BOOL_FROM_REPR) is True


def test_cant_set_attrs():
    # You can't set an attr on a constant.
    with pytest.raises(TypeError):
        constants.FISH_SLAPPING_DANCE.whatever = 4


def test_arithmetic():
    # Constants are repr'd by their name; simple.
    assert repr(constants.HOLY_HAND_GRENADE) == "HOLY_HAND_GRENADE"
    # If they have a representation set, that is added.
    constants.HOLY_HAND_GRENADE("One, Two, Five!")
    assert repr(constants.HOLY_HAND_GRENADE) == "HOLY_HAND_GRENADE (One, Two, Five!)"

    # They are added together by the value set for representation.
    constants.FORTY_TWO(42)
    assert 80 + constants.FORTY_TWO == 80 + 42

    # Adding strings to a constant with a string representation yields a string.
    constants.USERNAME("Bob")
    assert constants.USERNAME + " up and down in the water" == "Bob up and down in the water"

    # But adding bytes causes a cast to bytes.
    assert b"Sideshow " + constants.USERNAME == b'Sideshow Bob'

    # Same with int.
    constants.THIRTY_SEVEN(b"37")
    assert constants.THIRTY_SEVEN + 10 == 47

    # sub, mul, and truediv work also.
    assert constants.THIRTY_SEVEN - 30 == 7
    assert 137 - constants.THIRTY_SEVEN == 100

    assert constants.THIRTY_SEVEN * 2 == 74
    assert 3 * constants.THIRTY_SEVEN == 111

    assert constants.THIRTY_SEVEN / 4 == 9.25
    assert 111 / constants.THIRTY_SEVEN == 3.0


def test_constants_can_be_used_as_ints():
    constants.THREE(3)
    assert "humbug"[:constants.THREE] == "hum"


def test_constant_length():
    # The length of a constant is the length of its name...
    assert len(constants.PEAR) == 4

    # ...unless the representation is set, then it will be that length.
    constants.PEAR("fruit")
    assert len(constants.PEAR) == 5


def test_use_methods_on_representation():
    # By default, accessing strange attributes with raise AttributeError.
    with pytest.raises(AttributeError):
        constants.THE_OLD_MAN_THE_BOAT.upper()

    # If a representation is set, attributes other than ("__repr_content", "__bool_repr", "__name") pass through.
    constants.THE_OLD_MAN_THE_BOAT("when Fred eats food gets thrown.")
    assert constants.THE_OLD_MAN_THE_BOAT.upper() == 'WHEN FRED EATS FOOD GETS THROWN.'
