from pyttsx3 import init
import speech_recognition as sr

#from src import mod_volume
#from src import master_module
import mod_volume
import master_module

try:
    reco = sr.Recognizer()
    micro = sr.Microphone()

    engine = init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[41].id)
except OSError:
    reco = None
    micro = None
    print("Cannot define audio settings")

def speak(response) -> None:
    engine.say(response)
    engine.runAndWait()


def inputCommand() -> str:
    try:
        with micro as source:
            # r.pause_threshold = 3.0
            print("pronto ad ascoltare...")
            audio = reco.listen(source)

        question = reco.recognize_google(audio, language="it-IT").lower()
    except NameError:
        question = "question_name_ex"
    except AttributeError:
        question = "question_attribute_ex"
    except sr.UnknownValueError:
        question = "_NoQuestion"
    return question


def findModule(command: str) -> master_module.MasterModule: #MasterModule:
    module_volume = mod_volume.ModuleVolume() #ModuleVolume()

    if module_volume.check_command(command):
        return module_volume

    return None


def execute() -> bool:
    flag = False

    command = inputCommand()

    # print("Ecco cosa ho sentito")
    # print(command)
    # speak("Ecco cosa ho sentito")
    # speak(command)

    result = "Scusa, non so ancora come eseguire questo comando"

    if command == "stop":
        flag = True
        result = "Alla prossima!"
    elif command == "_NoQuestion":
        result = "Scusa, non ho capito"
    else:
        module = findModule(command)
        if module is not None:
            result = module.execute(command)

    speak(result)
    return flag


if __name__ == "__main__":
    stop = False

    while not stop:
        stop = execute()
