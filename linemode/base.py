class Printer(object):
    def compile(self, commands):
        """ Takes a list of commands and returns a program which can be
        printed using `execute`.

        The type and format of the returned program is private to the printer
        driver implementation.
        """
        raise NotImplementedError()

    def execute(self, program):
        """ Execute a compiled program.
        """
        raise NotImplementedError()

    def run_commands(self, commands):
        """ Shortcut for compiling and executing an iterator of commands
        """
        self.execute(self.compile(commands))

    def shutdown(self):
        pass
