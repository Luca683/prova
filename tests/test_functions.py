import sys
import os

src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_folder)

from pytest_mock import MockerFixture
import src.myAssistant




# We cannot test inputCommand(), beacuse the objects used in it are not defined during tests runned from a virtual environment
# def test_inputCommand(mocker: MockerFixture) -> None:
#     # arrange
#     mock_return = "Ciao moNdo"
#     mocker.patch.object(myAssistant.reco, "listen", return_value=mock_return)
#     mocker.patch.object(myAssistant.reco, "recognize_google", return_value=mock_return)

#     # act
#     res = myAssistant.inputCommand()

#     # assert
#     assert isinstance(res, str)
#     assert res == mock_return.lower()


def test_findModule():
    # assert
    res = src.myAssistant.findModule("abbassa volume di 150")
    #assert isinstance(res, ModuleVolume)
    res = src.myAssistant.findModule("Ciao mondo")
    assert res is None


def test_execution(mocker: MockerFixture) -> None:
    # arrange
    mock_return = "stop"
    mocker.patch.object(src.myAssistant, "inputCommand", return_value=mock_return)

    # Mock speak() or it will trigger during test
    mocker.patch.object(src.myAssistant, "speak", return_value=None)

    # act
    res = src.myAssistant.execute()

    # assert
    assert isinstance(res, bool)
    assert res is True
