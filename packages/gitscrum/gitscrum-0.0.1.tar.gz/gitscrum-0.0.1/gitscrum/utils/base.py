# Standard Library
import subprocess
from typing import List

# Third party
from termcolor import colored

# gitscrum
from gitscrum import __version__
from gitscrum.utils.warn import warn


class Base:
    def __init__(self, debug: bool = False, encoding: str = "utf-8"):
        self.debug = debug
        self.encoding = encoding
        self.date_format = "%Y-%m-%d"  # used for parsing, probably can't be configurable?

    def _get_shell_output(self, args: List[str]) -> str:
        # subprocess stdout is in bytes with trailing new line. need to decode and strip to get string back.
        # e.g. b'700aa82a2b0c\n' -> '700aa82a2b0c'
        if self.debug:
            print(colored(f"running command {args.join(' ')}", "blue"))

        return subprocess.check_output(args).decode(self.encoding).strip()

    def version(self):
        """
        Prints the version of gitscrum.
        """
        print(__version__)

    def current_user(self):
        user = self._get_shell_output(["git", "config", "user.email"])
        if not user:
            warn(
                'no git user found. please set `git config --global user.email "$YOUR_EMAIL"`',
                self.debug,
            )

        return user

    def has_commits(self):
        user = self.current_user()

        commits = self._get_shell_output(
            [
                "git",
                "log",
                "-1",  # only get one commit
                f"--author={user}",
            ]
        )

        if not commits:
            warn(f"No commits found for {user}")
            return False

        return True
