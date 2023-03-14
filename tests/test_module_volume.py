import sys
import os

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)

from typing import List
import pytest
from src.mod_volume import ModuleVolume, clamp_val

def test_clamp_val() -> None:
    assert isinstance(clamp_val(0), int)

    assert clamp_val(0) == 0
    assert clamp_val(100) == 100

    assert clamp_val(101) == 100
    assert clamp_val(-1) == 0


functionalities_tests: List[dict] = [
    # False commands
    {"command": "", "check_command_res": False},
    {"command": "test", "check_command_res": False},
    {"command": "alza di 10", "check_command_res": False},
    {"command": "metti a 10", "check_command_res": False},
    {"command": "metti volume a ", "check_command_res": False},
    # Set actions
    {
        "command": "metti volume a 10", "check_command_res": True, "expected_value": 10,
        "_set": True, "_update": False, "_to": True, "_by": False, "expected_res": "10%"
    },
    {
        "command": "setta volume a 90", "check_command_res": True, "expected_value": 90,
        "_set": True, "_update": False, "_to": True, "_by": False, "expected_res": "90%"
    },
    {
        "command": "imposta volume a 120", "check_command_res": True, "expected_value": 100,
        "_set": True, "_update": False, "_to": True, "_by": False, "expected_res": "100%"
    },
    # Update actions - By
    {
        "command": "alza volume di 10", "check_command_res": True, "expected_value": 10,
        "_set": False, "_update": True, "_to": False, "_by": True, "expected_res": "10%+"
    },
    {
        "command": "abbassa volume di 150", "check_command_res": True, "expected_value": 100,
        "_set": False, "_update": True, "_to": False, "_by": True, "expected_res": "100%-"
    },
    # Update actions - To
    {
        "command": "alza volume a 90", "check_command_res": True, "expected_value": 90,
        "_set": False, "_update": True, "_to": True, "_by": False, "expected_res": "90%"
    },
    {
        "command": "abbassa volume a 10", "check_command_res": True, "expected_value": 10,
        "_set": False, "_update": True, "_to": True, "_by": False, "expected_res": "10%"
    }
]


@pytest.mark.parametrize("test", functionalities_tests)
def test_functionalities(test: dict) -> None:
    m_volume = ModuleVolume()

    # Assert command check
    assert m_volume.check_command(test["command"]) == test["check_command_res"]

    # On False commands we don't want to assert further
    if not test["check_command_res"]:
        return

    # Assert properties
    assert m_volume.action_set == test["_set"]
    assert m_volume.action_update == test["_update"]
    assert m_volume.is_to == test["_to"]
    assert m_volume.is_by == test["_by"]
    assert m_volume.value == test["expected_value"]

    # Assert execution
    assert m_volume.find_new_volume(test["command"]) == test["expected_res"]
