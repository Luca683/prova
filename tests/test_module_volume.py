from typing import List
import pytest
import src.mod_volume as mod_volume

def test_clamp_val() -> None:
    assert type(mod_volume.clamp_val(0)) is int

    assert mod_volume.clamp_val(0) == 0
    assert mod_volume.clamp_val(100) == 100

    assert mod_volume.clamp_val(101) == 100
    assert mod_volume.clamp_val(-1) == 0


functionalities_tests: List[dict] = [
    # False commands
    {"command": "", "expected_res": False},
    {"command": "test", "expected_res": False},
    {"command": "alza di 10", "expected_res": False},
    {"command": "metti a 10", "expected_res": False},
    {"command": "metti volume a ", "expected_res": False},
    # Set actions
    {
        "command": "metti volume a 10", "expected_res": True, "expected_value": 10,
        "_set": True, "_update": False, "_to": True, "_by": False,
        "initial_val": 0.5, "end_val": 0.1
    },
    {
        "command": "setta volume a 90", "expected_res": True, "expected_value": 90,
        "_set": True, "_update": False, "_to": True, "_by": False,
        "initial_val": 0.5, "end_val": 0.9
    },
    {
        "command": "imposta volume a 120", "expected_res": True, "expected_value": 100,
        "_set": True, "_update": False, "_to": True, "_by": False,
        "initial_val": 0.5, "end_val": 1.0
    },
    # Update actions - By
    {
        "command": "alza volume di 10", "expected_res": True, "expected_value": 10,
        "_set": False, "_update": True, "_to": False, "_by": True,
        "initial_val": 0.5, "end_val": 0.6
    },
    {
        "command": "abbassa volume di 150", "expected_res": True, "expected_value": 100,
        "_set": False, "_update": True, "_to": False, "_by": True,
        "initial_val": 0.5, "end_val": 0.0
    },
    # Update actions - To
    {
        "command": "alza volume a 90", "expected_res": True, "expected_value": 90,
        "_set": False, "_update": True, "_to": True, "_by": False,
        "initial_val": 0.5, "end_val": 0.9
    },
    {
        "command": "abbassa volume a 10", "expected_res": True, "expected_value": 10,
        "_set": False, "_update": True, "_to": True, "_by": False,
        "initial_val": 0.5, "end_val": 0.1
    }
]


@pytest.mark.parametrize("test", functionalities_tests)
def test_functionalities(test: dict) -> None:
    m_volume = mod_volume.ModuleVolume()

    # Assert command check
    assert m_volume.check_command(test["command"]) == test["expected_res"]

    # On False commands we don't want to assert further
    if not test["expected_res"]:
        return

    # Assert properties
    assert m_volume.action_set == test["_set"]
    assert m_volume.action_update == test["_update"]
    assert m_volume.is_to == test["_to"]
    assert m_volume.is_by == test["_by"]
    assert m_volume.value == test["expected_value"]

    # Assert execution
    assert m_volume.find_new_volume(test["command"], test["initial_val"]) == test["end_val"]
