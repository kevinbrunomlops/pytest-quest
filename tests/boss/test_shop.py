
import pytest

from dungeon.hero import Hero
from dungeon.inventory import Inventory, InventoryFullError, Item
from dungeon.shop import (
    Listing,
    NotEnoughGoldError,
    OutOfStockError,
    Shop,
)


@pytest.fixture
def hero():
    return Hero("Ada", gold=100)


@pytest.fixture
def sword():
    return Item("Sword", weight=3.0, value=60)


@pytest.fixture
def shop(sword):
    return Shop([Listing(sword, price=30, stock=2)])


@pytest.mark.parametrize(
    "price, stock",
    [
        (-1, 1),
        (10, -1),
        (-1, -1),
    ],
)
def test_shop_rejects_negative_price_or_stock(sword, price, stock):
    shop = Shop()

    with pytest.raises(ValueError, match="non-negative"):
        shop.add_listing(Listing(sword, price=price, stock=stock))

    assert shop.stock_of("Sword") == 0


def test_shop_stock_of_unknown_item(shop):
    assert shop.stock_of("Unknown") == 0
    assert shop.stock_of("Sword") == 2


def test_shop_price_of_unknown_item(shop):
    with pytest.raises(OutOfStockError, match="doesn't sell"):
        shop.price_of("Unknown")


def test_shop_price_of_known_item(shop):
    assert shop.price_of("Sword") == 30


def test_buy_updates_gold_stock_and_inventory(hero, shop):
    inventory = Inventory()

    item = shop.buy(hero, inventory, "Sword")

    assert item.name == "Sword"
    assert hero.gold == 70
    assert shop.stock_of("Sword") == 1
    assert inventory.count("Sword") == 1


def test_buy_unknown_item_changes_nothing(hero, shop):
    inventory = Inventory()

    with pytest.raises(OutOfStockError):
        shop.buy(hero, inventory, "Unknown")

    assert hero.gold == 100
    assert shop.stock_of("Sword") == 2
    assert len(inventory) == 0


def test_buy_out_of_stock_changes_nothing(hero, sword):
    shop = Shop([Listing(sword, price=30, stock=0)])
    inventory = Inventory()

    with pytest.raises(OutOfStockError):
        shop.buy(hero, inventory, "Sword")

    assert hero.gold == 100
    assert shop.stock_of("Sword") == 0
    assert len(inventory) == 0


def test_buy_without_enough_gold_changes_nothing(shop):
    hero = Hero("Ada", gold=10)
    inventory = Inventory()

    with pytest.raises(NotEnoughGoldError):
        shop.buy(hero, inventory, "Sword")

    assert hero.gold == 10
    assert shop.stock_of("Sword") == 2
    assert len(inventory) == 0


def test_buy_when_inventory_is_full_changes_nothing(hero, shop):
    inventory = Inventory(max_weight=1)

    with pytest.raises(InventoryFullError):
        shop.buy(hero, inventory, "Sword")

    assert hero.gold == 100
    assert shop.stock_of("Sword") == 2
    assert len(inventory) == 0


def test_sell_known_item_increases_shop_stock(hero, shop, sword):
    inventory = Inventory()
    inventory.add(sword)

    payout = shop.sell(hero, inventory, "Sword")

    assert payout == 30
    assert hero.gold == 130
    assert shop.stock_of("Sword") == 3
    assert inventory.count("Sword") == 0


def test_sell_unknown_shop_item_does_not_create_listing(hero, shop):
    inventory = Inventory()
    shield = Item("Shield", weight=2.0, value=41)
    inventory.add(shield)

    payout = shop.sell(hero, inventory, "Shield")

    assert payout == 20
    assert hero.gold == 120
    assert shop.stock_of("Shield") == 0
    assert inventory.count("Shield") == 0
