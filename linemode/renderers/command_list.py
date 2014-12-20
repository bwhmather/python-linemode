import ast
import re


def render(source):
    for line in source.splitlines():
        if re.match(r"(^#.*)$|^$", line):
            # line is empty or a comment, skip
            continue

        elif re.match(r"^[a-z\-]+$", line):
            # line is a single command
            yield line.strip()

        elif re.match(r"^[a-z\-]+:", line):
            # line is a command with arguments
            command, args = line.split(':', 1)
            args = ast.literal_eval('(%s,)' % args)

            yield (command,) + args
