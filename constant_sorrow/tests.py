import pytest

from constant_sorrow import constants


def test_establishing_a_constant():
    # You get a constant by just picking an all-caps name and importing it.
    from constant_sorrow.constants import THIS_IS_A_VALID_CONSTANT

    # That name didn't exist before - you literally just make up
    # an all-caps name and import it.

    # But you can't make a constant in lower case.
    with pytest.raises(ValueError):
        constants.this_is_not_the_right_case_for_a_constant


def test_different_constants_are_unequal():
    # Constants with different names are not equal to each other by default.
    assert constants.ONE_THING != constants.ANOTHER_THING


def test_same_constants_are_identical():
    # However, constants with the same name are both equal and identical to one another.
    # They are literally the same object.
    from constant_sorrow.constants import SAME_THING
    assert constants.SAME_THING == SAME_THING
    assert constants.SAME_THING is SAME_THING


def test_set_representation():
    # Merely using a constant as a special value flag might not be enough.
    # You might want to represent it for the purposes of, for example,
    # sending it over the wire as bytes.
    from constant_sorrow.constants import AFRICAN_SWALLOW
    AFRICAN_SWALLOW(b"non-migratory")
    assert bytes(AFRICAN_SWALLOW) == b"non-migratory"


def test_bytes_representation_default():
    """By default, constants are represented as a SHA512 hash of their name, truncated to 8 bytes."""
    another_constant = constants.ANOTHER_CONSTANT
    assert len(bytes(another_constant)) == 8
    assert bytes(another_constant) == constants.ANOTHER_CONSTANT


def test_cast_representation():
    constants.FOURTEEN(b"14")

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
    # (because it's a Constant - it'd be bizarre behavior for the bool representation to change)
    constants.WITH_SET_BOOL("this string is non-empty, but this constant is still False.")
    assert bool(constants.WITH_SET_BOOL) is False

    # You can set it to the same value again...
    constants.WITH_BOOL.bool_value(False)

    # But you can't change the bool value once set.
    with pytest.raises(ValueError):
        constants.WITH_BOOL.bool_value(True)

    # Also, we can't take the first constant above and set its bool value to False.
    # It was True before, because prior to it having a bool_value, it was represented
    # by a non-empty string.  So now, we can't change it to False.
    # After all - we want it to act like a constant.
    with pytest.raises(ValueError):
        constants.WITH_BOOL_FROM_REPR.bool_value(False)

    # We can, however, set it to True, because its current value is True.
    constants.WITH_BOOL_FROM_REPR.bool_value(True)
    assert bool(constants.WITH_BOOL_FROM_REPR) is True


def test_str_representation():
    # By default, Constants cast to str as their name:
    str(constants.BECAUSE_IT_IS_MY_NAME) == "BECAUSE_IT_IS_MY_NAME"

    # If a Constant is ever cast this way, its representation can't be changed to
    # an object whose string representation is different.
    # For example, this object that casts to the same string:

    class BecauseICannotHaveAnotherInMyLife:
        def __str__(self):
            return "BECAUSE_IT_IS_MY_NAME"

    constants.BECAUSE_IT_IS_MY_NAME(BecauseICannotHaveAnotherInMyLife())

    # ...but this one will not cast away its good name, sir:
    class AbigailWilliams:
        def __str__(self):
            return "Mylène Demongeot"

    str(constants.WINONA_RYDER)

    with pytest.raises(ValueError):
        constants.WINONA_RYDER(AbigailWilliams())

    # Note: it's possible to use an object which initially has a str repr that matches, but later changes.
    # This is almost certainly a bad idea, but if you're going to go that far, we trust you have a reason.
    class BecauseILieAndSignMyselfToLies:
        name = "JOHN PROCTOR"

        def __str__(self):
            return self.name

    constants.JOHN_PROCTOR(BecauseILieAndSignMyselfToLies())
    BecauseILieAndSignMyselfToLies.name = "Daniel Plainview"
    assert str(constants.JOHN_PROCTOR) == "Daniel Plainview"
    # ...but again, why?  This seems like a bad idea, but it's also not the place
    # of the Constant class to police the internal behavior of your classes.


def test_cant_set_attrs():
    # You can't set an attr on a constant.
    with pytest.raises(TypeError):
        constants.FISH_SLAPPING_DANCE.whatever = 4


def test_repr_as_str():
    # Constants are repr'd by their name; simple.
    from constant_sorrow.constants import HOLY_HAND_GRENADE
    assert repr(HOLY_HAND_GRENADE) == "HOLY_HAND_GRENADE"
    # If they have a representation set, that is added.
    HOLY_HAND_GRENADE("One, Two, Five!")
    assert repr(HOLY_HAND_GRENADE) == "HOLY_HAND_GRENADE (One, Two, Five!)"


def test_arithmetic():
    # Constants are summed by their representation.
    constants.FORTY_TWO(42)
    assert 80 + constants.FORTY_TWO == 80 + 42

    # Adding strings to a constant with a string representation yields a string.
    from constant_sorrow.constants import ROBERT
    ROBERT("Bob")
    assert ROBERT + " up and down in the water" == "Bob up and down in the water"

    # But adding bytes causes a cast to bytes.
    assert b"Sideshow " + ROBERT == b'Sideshow Bob'

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
    # A constant which is represented as an int can be used in most places
    # that an int can be used, even without casting first.
    constants.THREE(3)
    assert "humbug"[:constants.THREE] == "hum"


def test_constant_length():
    # By default, the length of a constant is the length of its name...
    assert len(constants.PEAR) == 4

    # ...but once a representation is set, then it will be that length.
    constants.PEAR("fruit")
    assert len(constants.PEAR) == 5


def test_iterable_constant():
    # Setup a new iterable constant of string literals
    names = ('Ron', 'Bob', 'Jerry', 'Phil', 'Keith', 'Donna')
    constants.MEMBERS(names)

    # The constant can be cast to a list...
    assert list(constants.MEMBERS) == list(names)

    # python 3.6 test
    # pigpen, *the_rest = list(constants.MEMBERS)
    # assert pigpen == 'Ron'
    # assert len(the_rest) == 5

    # ...unpacked into a function.
    def take_input_and_do_nothing_with_it(a, b, c, d, e, f): return True

    assert take_input_and_do_nothing_with_it(*constants.MEMBERS)

    # Hold a collection of constants...
    _weather = (constants.THUNDER('⛈'),
                constants.LIGHTNING('⚡'),
                constants.WIND('💨'),
                constants.RAIN('💧'))

    constants.WEATHER(_weather)

    def operate_on_input(a, b, c, d):
        assert a + b + c + d == '⛈⚡💨💧'
        return True

    # ...unpack and operate on the elements directly...
    assert operate_on_input(*constants.WEATHER)

    # ...or iterate over the constant
    assert ''.join(str(item) for item in constants.WEATHER) == '⛈⚡💨💧'


def test_use_methods_on_representation():
    # By default, accessing strange attributes with raise AttributeError.
    from constant_sorrow.constants import THE_OLD_MAN_THE_BOAT
    with pytest.raises(AttributeError):
        THE_OLD_MAN_THE_BOAT.upper()

    # If a representation is set, attributes other than ("__repr_content", "__bool_repr", "__name") pass through.
    THE_OLD_MAN_THE_BOAT("when Fred eats food gets thrown.")
    assert THE_OLD_MAN_THE_BOAT.upper() == 'WHEN FRED EATS FOOD GETS THROWN.'


def test_useful_name_in_exception_output():
    """
    Constants use a metaclass which uses the Constant name as the string representation of the class (not only the instance).
    This is useful for meaningful error messages.
    """
    try:
        constants.NORTHERN_RAILROAD[:7]
    except TypeError as e:
        assert e.args[0] == "'NORTHERN_RAILROAD' object is not subscriptable"
    else:
        pytest.fail("Expected this constant not to be subscriptable by default.")
