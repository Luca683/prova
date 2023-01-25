from pytest_mock import MockerFixture
from src.mod_volume import ModuleVolume
import src.myAssistant as myAssistant

def test_inputCommand(mocker: MockerFixture) -> None:
    # arrange
    mock_return = "Ciao moNdo"
    mocker.patch.object(myAssistant.reco, "listen", return_value=mock_return)
    mocker.patch.object(myAssistant.reco, "recognize_google", return_value=mock_return)

    # act
    res = myAssistant.inputCommand()

    # assert
    assert isinstance(res, str)
    assert res == mock_return.lower()


def test_findModule():
    # assert
    res = myAssistant.findModule("abbassa volume di 150")
    assert isinstance(res, ModuleVolume)
    res = myAssistant.findModule("Ciao mondo")
    assert res is None


def test_execution(mocker: MockerFixture) -> None:
    # arrange
    mock_return = "stop"
    mocker.patch.object(myAssistant, "inputCommand", return_value=mock_return)

    # Mock speak() or it will trigger during test
    mocker.patch.object(myAssistant, "speak", return_value=None)

    # act
    res = myAssistant.execute()

    # assert
    assert isinstance(res, bool)
    assert res is True