from unittest.mock import patch
from cs314_group_project.member import Member, MemberStatus
import json


# Testing Jessie's information
@patch("builtins.input", side_effect=["Jessie", "Le"])
def test_valid_input_name(_):
    member = Member()
    member.input_name()
    assert member.full_name == "Jessie Le"


@patch("builtins.input", side_effect=["5840 SW 166th Ct", "Beaverton", "Oregon", 12345])
def test_valid_input_address(_):
    member = Member()
    member.input_address()
    assert member.street == "5840 SW 166th Ct"
    assert member.city == "Beaverton"
    assert member.state == "Oregon"
    assert member.zip == 12345


@patch("random.randint", side_effect=[12345678])
def test_input_member_number(_):
    member = Member()
    member.input_member_number()
    assert member.member_number == 12345678
    assert isinstance(member.member_number, int)


# testing address update
@patch("builtins.input", side_effect=["9735 SW Shady Lane", "Tigard", "Oregon", 97223])
def test_address_update(_):
    member = Member()
    member.update_address("Mia Harris")
    if member.full_name == "Mia Harris":
        assert member.street == "9735 SW Shady Lane"
        assert member.city == "Tigard"
        assert member.state == "Oregon"
        assert member.zip == 97223


def test_member_search_valid():
    member = Member()
    testnum = 927517086
    result = member.search_member(testnum)
    assert result == MemberStatus.VALIDATED


def test_member_search_suspend():
    member = Member()
    testnum = 983659929
    result = member.search_member(testnum)
    assert result == MemberStatus.SUSPENDED


def test_member_search_notfound():
    member = Member()
    testnum = 111111111
    result = member.search_member(testnum)
    assert result == MemberStatus.NOT_FOUND


def test_check_mem_exist():
    member = Member()
    directory = "member_list.json"
    try:
        with open(directory) as file:
            member_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Member directory not found or empty.")
        return
    testnum = 983659929
    result = member.check_member_exist(testnum, member_list)
    assert result is True


def test_check_mem_not_exist():
    member = Member()
    directory = "member_list.json"
    try:
        with open(directory) as file:
            member_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Member directory not found or empty.")
        return
    testnum = 111111111
    result = member.check_member_exist(testnum, member_list)
    assert result is False
