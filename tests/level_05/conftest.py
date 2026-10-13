import pytest

from dungeon.hero import Hero
from dungeon.inventory import Inventory, Item
from dungeon.shop import Listing, Shop

@pytest.fixture
def hero():
    return Hero("Ada", gold=100)

@pytest.fixture
def backpack():
    return Inventory(max_weight=10.0)

@pytest.fixture
def sword():
    return Item("Sword", weight=3.0, value=51)

@pytest.fixture
def shop(sword):
    return Shop([
        Listing(item=sword, price=30, stock=2)
    ])

@pytest.fixture
def poor_hero(hero):
    hero.gold = 5
    return hero