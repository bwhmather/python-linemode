from abc import ABCMeta


class Printer(metaclass=ABCMeta):
    def run_commands(self, commands):
        pass
