from unittest.mock import patch
from cs314_group_project.provider import Provider

# import json


@patch("builtins.input", side_effect=["Jessie", "Le"])
def test_valid_input_name(_):
    prov = Provider()
    prov.input_name()
    assert prov.full_name == "Jessie Le"


@patch("builtins.input", side_effect=["5840 SW 166th Ct", "Beaverton", "Oregon", 12345])
def test_valid_input_address(_):
    prov = Provider()
    prov.input_address()
    assert prov.street == "5840 SW 166th Ct"
    assert prov.city == "Beaverton"
    assert prov.state == "Oregon"
    assert prov.zip == 12345


@patch("random.randint", side_effect=[12345678])
def test_input_provider_number(_):
    prov = Provider()
    prov.input_provider_number()
    assert prov.provider_number == 12345678
    assert isinstance(prov.provider_number, int)


@patch("builtins.input", side_effect=["9735 SW Shady Lane", "Tigard", "Oregon", 97223])
def test_address_update(_):
    prov = Provider()
    prov.update_address()
    if prov.full_name == "Mia Harris":
        assert prov.street == "9735 SW Shady Lane"
        assert prov.city == "Tigard"
        assert prov.state == "Oregon"
        assert prov.zip == 97223
