# Standard Library
import subprocess
from datetime import datetime

# Third party
from termcolor import (  # TODO: switch to color class? open source + windows https://pypi.org/project/colorclass/
    colored,
)
from terminaltables import AsciiTable

# gitscrum
from gitscrum.utils.base import Base


class Standup(Base):
    def standup(self, warnings: bool = True, output_format: str = "%h %s") -> str:
        """
        Returns the commits for today and yesterday or last commit before today if available.

        Args:
            warnings: toggle display of warnings
            output_format: git commit format. default is short hash and commit message (%h %s).
                           note color output is not preserved by subprocess so %C
        """
        user = self.current_user()
        self.has_commits()

        last_commit_date_before_today = self._get_shell_output(
            [
                "git",
                "log",
                "-1",  # only get one commit
                f"--author={user}",
                "--before=yesterday.midnight",
                "--format=%ad",
                f"--date=format:{self.date_format}",  # YYYY-mm-dd
            ]
        )

        parsed_last_date = datetime.strptime(last_commit_date_before_today, self.date_format)
        # TODO: humanize date if possible
        # TODO: don't show author in commit, just hash and message
        # TODO: show commits on multiple branches?
        #           maybe all on main branch (master? parse?) then summary from feature branches?
        # TODO: enumerate commits
        # TODO: open with pager?
        # TODO: fix arg parsing from __init__.py

        commits_before_today = self._get_shell_output(
            [
                "git",
                "log",
                "--all",
                f"--author={user}",
                f"--after={parsed_last_date}",
                "--before=today.midnight",
                f"--format={output_format}"
            ]
        )

        commits_today = self._get_shell_output(
            [
                "git",
                "log",
                "--all",
                f"--author={user}",
                "--after=today.midnight",
                f"--format={output_format}"
            ]
        )

        headers = []
        body = []

        if commits_before_today:
            headers.append(colored(last_commit_date_before_today, "green"))
            body.append(commits_before_today)
        else:
            if warnings:
                print(colored("No commits found before today.", "yellow"))

        if commits_today:
            headers.append(colored("today", "green"))
            body.append(commits_today)
        else:
            if warnings:
                print(colored("No commits found today", "yellow"))

        title = "standup"
        table = AsciiTable([headers, body], title)
        print(table.table)
