from abc import ABCMeta


class Printer(metaclass=ABCMeta):
    def run_commands(self, commands):
        pass

    def shutdown(self):
        pass
