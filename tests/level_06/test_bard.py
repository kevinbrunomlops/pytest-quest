from dungeon.bard import sing_of
from dungeon.hero import Hero

def test_bard_sings_to_stdout(capsys):
    hero = Hero("Ada", level=3)

    sing_of(hero)

    captured = capsys.readouterr()

    assert "Hear the tale of Ada, a level 3 hero!" in captured.out
    assert captured.err == ""

def test_bard_mentions_rich_hero(capsys):
    hero = Hero("Ada", gold=150)

    sing_of(hero)

    captured = capsys.readouterr()

    assert "Ada carries 150 gold" in captured.out
    assert captured.err == ""

def test_bard_warns_about_wounded_hero(capsys):
    hero = Hero("Ada", hp=20, max_hp=100)

    sing_of(hero)

    captured = capsys.readouterr()

    assert "Hear the tale of Ada" in captured.out
    assert "Ada does not look so good" in captured.err

def test_bard_does_not_warn_at_25_percent_hp(capsys):
    hero = Hero("Ada", hp=25, max_hp=100)

    sing_of(hero)

    captured = capsys.readouterr()

    assert captured.err == ""