from cs314_group_project.terminal import Terminal
from cs314_group_project.manager_terminal import Manager
from cs314_group_project.provider_terminal import ProviderTerm
from unittest.mock import patch


def test_assign_type1():
    setup = Terminal()
    setup.assign_type(1)
    assert setup.type == "Provider"


def test_assign_type2():
    setup = Terminal()
    setup.assign_type(2)
    assert setup.type == "Manager"


def test_assign_type3():
    setup = Terminal()
    setup.assign_type(3)
    assert setup.type == "Quit"


def test_assign_typenone():
    setup = Terminal()
    setup.assign_type(4)
    assert setup.type is None


@patch("builtins.input", side_effect=["1"])
def test_man_main_menu1(_):
    setup = Manager()
    result = setup.option_menu()
    assert result == 1


@patch("builtins.input", side_effect=["1"])
def test_man_provider_menu1(_):
    setup = Manager()
    result = setup.provider_menu()
    assert result == 1


@patch("builtins.input", side_effect=["1"])
def test_man_member_menu1(_):
    setup = Manager()
    result = setup.member_menu()
    assert result == 1


@patch("builtins.input", side_effect=["1"])
def test_man_report_menu1(_):
    setup = Manager()
    result = setup.report_menu()
    assert result == 1


@patch("builtins.input", side_effect=["1"])
def test_prov_main_menu1(_):
    setup = ProviderTerm()
    result = setup.option_menu()
    assert result == 1
