import subprocess
import re
import importlib
master_module = importlib.import_module('master_module')
#from master_module import MasterModule



# Clamp values between 0 and 100
def clamp_val(number: int) -> int:
    if number < 0:
        return 0

    if number > 100:
        return 100

    return number


class ModuleVolume(master_module.MasterModule):
    def __init__(self):
        self.action_set = False
        self.is_to = False
        self.action_update = False
        self.is_by = False
        self.value = -1

    def check_command(self, command: str) -> bool:
        set_regex = r"\b(?P<command>metti|imposta|setta)\b.*?\bvolume\b.+?\ba\b.+?\b(?P<value>\d+)\b"

        if (match := re.search(set_regex, command)) is not None:
            value = int(match.group("value"))
            self.value = clamp_val(value)
            self.action_set = True
            self.is_to = True
            return True

        update_regex = r"\b(?P<command>alza|abbassa)\b.*?\bvolume\b.+?\b(?P<selector>a|di)\b.+?\b(?P<value>\d+)\b"

        if (match := re.search(update_regex, command)) is not None:
            value = int(match.group("value"))
            self.value = clamp_val(value)
            self.is_to = match.group("selector") == "a"
            self.is_by = not self.is_to
            self.action_update = True
            return True

        return False

    def execute(self, command: str) -> str:
        try:
            val = self.find_new_volume(command)
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", val], check=True)

        except OSError:
            return "There was a problem with the SO"

        return "Ho modificato il volume"

    # Returns a nev volume value in the range [0,1]
    def find_new_volume(self, command: str) -> float:
        # "... [Setta / Alza / Imposta]/[Alza / Abbassa] ... A ..."
        if self.is_to and (self.action_set or self.action_update):
            return str(self.value) + "%"

        # "... [Alza / Abbassa] ... DI ..."
        if self.is_by and self.action_update:
            # Current volume
            val = str(self.value) + "%"

            # Up or down?
            if "alza" in command:
                val += "+"
            elif "abbassa" in command:
                val += "-"

            return val

        # Should not happen
        return str(self.value) + "%"
