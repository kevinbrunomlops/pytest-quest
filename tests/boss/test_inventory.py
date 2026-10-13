
import pytest

from dungeon.inventory import Inventory, InventoryFullError, Item


@pytest.fixture
def inventory():
    return Inventory(max_weight=10)


@pytest.fixture
def sword():
    return Item(name="Sword", weight=3.0, value=100)


@pytest.fixture
def potion():
    return Item(name="Potion", weight=0.5, value=25)


@pytest.mark.parametrize("max_weight", [0, -1, -10])
def test_inventory_rejects_invalid_max_weight(max_weight):
    with pytest.raises(ValueError, match="must be positive"):
        Inventory(max_weight=max_weight)


@pytest.mark.parametrize("quantity", [0, -1])
def test_add_rejects_invalid_quantity(inventory, sword, quantity):
    with pytest.raises(ValueError, match="at least 1"):
        inventory.add(sword, quantity=quantity)

    assert len(inventory) == 0


def test_add_rejects_items_exceeding_weight_limit(inventory, sword):
    inventory.add(sword, quantity=3)

    with pytest.raises(InventoryFullError, match="too heavy"):
        inventory.add(sword)

    assert inventory.count("Sword") == 3
    assert inventory.total_weight == 9.0


def test_add_allows_exact_weight_limit(inventory):
    heavy_item = Item("Armor", weight=10.0, value=200)

    inventory.add(heavy_item)

    assert inventory.total_weight == 10.0
    assert inventory.count("Armor") == 1


def test_add_same_item_multiple_times(inventory, potion):
    inventory.add(potion, quantity=2)
    inventory.add(potion, quantity=3)

    assert inventory.count("Potion") == 5
    assert len(inventory) == 5


def test_remove_rejects_missing_item(inventory):
    with pytest.raises(LookupError, match="not enough"):
        inventory.remove("Missing")

    assert len(inventory) == 0


def test_remove_rejects_insufficient_quantity(inventory, sword):
    inventory.add(sword, quantity=2)

    with pytest.raises(LookupError, match="not enough"):
        inventory.remove("Sword", quantity=3)

    assert inventory.count("Sword") == 2


def test_remove_partial_quantity(inventory, potion):
    inventory.add(potion, quantity=4)

    removed = inventory.remove("Potion", quantity=2)

    assert removed is potion
    assert inventory.count("Potion") == 2
    assert inventory.find("Potion") is potion


def test_remove_all_copies(inventory, sword):
    inventory.add(sword, quantity=2)

    removed = inventory.remove("Sword", quantity=2)

    assert removed is sword
    assert inventory.count("Sword") == 0
    assert inventory.find("Sword") is None
    assert "Sword" not in inventory
    assert len(inventory) == 0


def test_inventory_count_and_find(inventory, sword):
    assert inventory.count("Sword") == 0
    assert inventory.find("Sword") is None

    inventory.add(sword)

    assert inventory.count("Sword") == 1
    assert inventory.find("Sword") is sword


def test_inventory_names_are_sorted(inventory):
    inventory.add(Item("Zebra", 1.0))
    inventory.add(Item("Apple", 1.0))

    assert inventory.names() == ["Apple", "Zebra"]


def test_inventory_as_dict(inventory, sword, potion):
    inventory.add(sword, quantity=2)
    inventory.add(potion, quantity=3)

    assert inventory.as_dict() == {
        "Sword": 2,
        "Potion": 3,
    }


def test_inventory_total_weight_and_value(inventory, sword, potion):
    inventory.add(sword, quantity=2)
    inventory.add(potion, quantity=3)

    assert inventory.total_weight == pytest.approx(7.5)
    assert inventory.total_value == 275


def test_inventory_length_and_contains(inventory, sword, potion):
    inventory.add(sword, quantity=2)
    inventory.add(potion, quantity=1)

    assert len(inventory) == 3
    assert "Sword" in inventory
    assert "Potion" in inventory
    assert "Shield" not in inventory
