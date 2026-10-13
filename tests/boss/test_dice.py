
import random

import pytest

from dungeon import dice


@pytest.mark.parametrize("sides", [0, 1, -1])
def test_roll_rejects_invalid_sides(sides):
    with pytest.raises(ValueError, match="at least 2 sides"):
        dice.roll(sides)


def test_roll_with_seeded_random_generator():
    rng1 = random.Random(7)
    rng2 = random.Random(7)

    results1 = [dice.roll(6, rng1) for _ in range(10)]
    results2 = [dice.roll(6, rng2) for _ in range(10)]

    assert results1 == results2
    assert all(1 <= result <= 6 for result in results1)


def test_roll_without_custom_rng():
    result = dice.roll(6)

    assert 1 <= result <= 6


def test_roll_notation_with_seeded_rng():
    rng = random.Random(7)
    expected_rng = random.Random(7)

    expected = sum(expected_rng.randint(1, 6) for _ in range(2)) + 3

    result = dice.roll_notation("2d6+3", rng=rng)

    assert result == expected


def test_roll_notation_without_modifier():
    rng = random.Random(42)
    expected_rng = random.Random(42)

    expected = expected_rng.randint(1, 20)

    result = dice.roll_notation("d20", rng=rng)

    assert result == expected


def test_roll_notation_rejects_invalid_notation():
    with pytest.raises(ValueError, match="invalid dice notation"):
        dice.roll_notation("not-a-dice")
