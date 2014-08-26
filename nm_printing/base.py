from abc import ABCMeta


class Printer(metaclass=ABCMeta):
    def compile(self, commands):
        """ Takes a list of commands and returns a program which can be
        printed using `execute`.

        The type and format of the returned program is private to the printer
        driver implementation.
        """
        pass

    def execute(self, program):
        """ Execute a compiled program.
        """
        pass

    def shutdown(self):
        pass
