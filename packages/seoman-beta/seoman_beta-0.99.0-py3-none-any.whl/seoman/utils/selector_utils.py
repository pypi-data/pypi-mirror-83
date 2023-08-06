import inquirer  # type: ignore
from typing import List, Any
from .config_utils import ALL_GRANULARITIES
from time import strftime, strptime
import typer


def create_selector(key: str, message: str, choices: List) -> Any:
    """
    Generic function that creates a dropdown selector from any list.
    """

    questions = [inquirer.List(name=key, message=message, choices=choices)]
    answer = inquirer.prompt(questions)
    return answer[key]


def create_granularity_selector(start: str, end: str) -> str:
    """Create a dropdown selector for granularity & frequency."""

    start, end = strftime("%d %b %Y", strptime(start, "%Y-%m-%d")), strftime(
        "%d %b %Y", strptime(end, "%Y-%m-%d")
    )

    questions = [
        inquirer.List(
            name="granularity",
            message=f"How frequently you would like to get your data between {start} and {end}",
            choices=ALL_GRANULARITIES,
        )
    ]

    answer = inquirer.prompt(questions)
    return answer["granularity"]
