
import pytest

from dungeon.hero import Hero


@pytest.mark.parametrize("max_hp", [0, -1, -100])
def test_hero_rejects_invalid_max_hp(max_hp):
    with pytest.raises(ValueError, match="max_hp must be positive"):
        Hero("Ada", max_hp=max_hp)


@pytest.mark.parametrize("amount", [-1, -10, -100])
def test_hero_rejects_negative_healing(amount):
    hero = Hero("Ada", max_hp=100, hp=50)

    with pytest.raises(ValueError, match="healing cannot be negative"):
        hero.heal(amount)

    assert hero.hp == 50


@pytest.mark.parametrize("amount", [-1, -50, -100])
def test_hero_rejects_negative_xp(amount):
    hero = Hero("Ada", xp=50)

    with pytest.raises(ValueError, match="xp cannot be negative"):
        hero.gain_xp(amount)

    assert hero.xp == 50
    assert hero.level == 1
