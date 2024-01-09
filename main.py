import argparse
from population_demographics import make_demographic_tables


def manage_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--race-demographics", action="store_true", help="", default=False
    )
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


def main(args: argparse.Namespace) -> None:
    print(f"main started with {args=}")

    if args.race_demographics:
        table, pop_table = make_demographic_tables(args)
        print("------HISTORICAL POPULATION COPY BELOW------\n")
        print(pop_table)
        print("\n\n")
        print(table)
        print("------RACE DEMOGRAPHICS COPY ABOVE------\n")
    else:
        print("Missing args")


if __name__ == "__main__":
    args = manage_cli_args()
    main(args)
