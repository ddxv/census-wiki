"""Main contains start point for running from command line."""
import argparse

from logger import get_logger
from population_demographics import make_demographic_tables

logger = get_logger(__name__)


def manage_cli_args() -> argparse.Namespace:
    """Set command line interface arguments for running file."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--state-abbr",
        action="store",
        help="State abbreviation like: AL or NY",
    )
    parser.add_argument(
        "-p",
        "--place-name",
        action="store",
        help="Single name of Census Designated Place like New York",
    )
    args, leftovers = parser.parse_known_args()
    return args


def main(cli_args: argparse.Namespace) -> None:
    """Print Wiki tables based on command line arguments."""
    logger.info(f"Started with {cli_args=}")

    table, pop_table = make_demographic_tables(cli_args)
    copy_pastable_msg = ""
    copy_pastable_msg += "\n------HISTORICAL POPULATION COPY BELOW------\n"
    copy_pastable_msg += pop_table
    copy_pastable_msg += "\n\n"
    copy_pastable_msg += table
    copy_pastable_msg += "\n\n------RACE DEMOGRAPHICS COPY ABOVE------\n"
    logger.info(copy_pastable_msg)


if __name__ == "__main__":
    args = manage_cli_args()
    main(args)
