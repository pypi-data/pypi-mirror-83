"""
A CLI for scrum tasks with git
"""

__version__ = "0.0.1"


# Third party
import fire

# gitscrum
from gitscrum.retro import Retro
from gitscrum.standup import Standup
from gitscrum.utils.base import Base


def main():
    fire.Fire({"standup": Standup().standup, "retro": Retro().retro})


if __name__ == "__main__":
    main()
