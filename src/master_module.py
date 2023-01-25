from abc import ABC, abstractmethod


class MasterModule(ABC):

    # Returns true if this module can execute the command given in input
    @abstractmethod
    def check_command(self, command: str) -> bool:
        pass

    # Execute the command and returns the outcome of the execution as a string
    @abstractmethod
    def execute(self, command: str) -> str:
        pass
