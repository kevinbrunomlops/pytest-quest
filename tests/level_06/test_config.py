
import pytest

from dungeon.config import difficulty, monster_hp


def test_default_difficulty(monkeypatch):
    monkeypatch.delenv("DUNGEON_DIFFICULTY", raising=False)

    assert difficulty() == "normal"
    assert monster_hp(100) == 100


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("easy", "easy", id="easy"),
        pytest.param("HARD", "hard", id="uppercase"),
        pytest.param(" Normal ", "normal", id="surrounding-spaces"),
        pytest.param("  HaRd  ", "hard", id="mixed-case-and-spaces"),
    ],
)
def test_difficulty_normalizes_input(monkeypatch, value, expected):
    monkeypatch.setenv("DUNGEON_DIFFICULTY", value)

    assert difficulty() == expected


@pytest.mark.parametrize(
    ("difficulty_value", "expected_hp"),
    [
        pytest.param("easy", 50, id="easy-half-hp"),
        pytest.param("normal", 100, id="normal-hp"),
        pytest.param("hard", 200, id="hard-double-hp"),
    ],
)
def test_monster_hp_multiplier(monkeypatch, difficulty_value, expected_hp):
    monkeypatch.setenv("DUNGEON_DIFFICULTY", difficulty_value)

    assert monster_hp(100) == expected_hp


def test_monster_hp_is_at_least_one(monkeypatch):
    monkeypatch.setenv("DUNGEON_DIFFICULTY", "easy")

    assert monster_hp(1) == 1


def test_unknown_difficulty_raises_value_error(monkeypatch):
    monkeypatch.setenv("DUNGEON_DIFFICULTY", "impossible")

    with pytest.raises(ValueError, match="unknown difficulty"):
        difficulty()
