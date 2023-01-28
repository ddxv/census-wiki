import pandas as pd
from census import Census
from us import states
from wiki import df_to_wikitable
from config import API_KEY
import argparse


CENSUS_REFERNCE_URL = "https://data.census.gov/table?g=1600000US{state_fips}{place_id}&y={year}&d=DEC+Redistricting+Data+(PL+94-171)&tid=DECENNIALPL{year}"

HISPANIC = "[[Hispanic and Latino Americans|Hispanic or Latino (of any race)]]"
WHITE_NH = "[[Non-Hispanic whites|White (non-Hispanic)]]"
BLACK_NH = "[[African American|Black or African American (non-Hispanic)]]"
AM_INDIAN_NH = (
    "[[Native Americans in the United States|Native American (non-Hispanic)]]"
)
ASIAN_NH = "[[Asian American|Asian (non-Hispanic)]]"
PACIF_NH = "[[Pacific Islander Americans|Pacific Islander (non-Hispanic)]]"
OTHER_NH = "Other (non-Hispanic)"
MULTI_NH = "[[Multiracial American|Two or more races (non-Hispanic)]]"


P2_2020 = {
    # https://api.census.gov/data/2020/dec/pl/groups/P2.html
    "P2_001N": "total",
    "P2_002N": HISPANIC,
    "P2_005N": WHITE_NH,
    "P2_006N": BLACK_NH,
    "P2_007N": AM_INDIAN_NH,
    "P2_008N": ASIAN_NH,
    "P2_009N": PACIF_NH,
    "P2_010N": OTHER_NH,
    "P2_011N": MULTI_NH,
}

P2_2010 = {
    # https://api.census.gov/data/2010/dec/pl/groups/P2.html
    "P002001": "total",
    "P002002": HISPANIC,
    "P002005": WHITE_NH,
    "P002006": BLACK_NH,
    "P002007": AM_INDIAN_NH,
    "P002008": ASIAN_NH,
    "P002009": PACIF_NH,
    "P002010": OTHER_NH,
    "P002011": MULTI_NH,
}

P2_2000 = {
    # https://api.census.gov/data/2000/dec/pl/groups/PL002.html
    "PL002001": "total",
    "PL002002": HISPANIC,
    "PL002005": WHITE_NH,
    "PL002006": BLACK_NH,
    "PL002007": AM_INDIAN_NH,
    "PL002008": ASIAN_NH,
    "PL002009": PACIF_NH,
    "PL002010": OTHER_NH,
    "PL002011": MULTI_NH,
}


def append_citation_to_columns(df: pd.DataFrame, state_fips, place_id) -> pd.DataFrame:
    for year in [2000, 2010, 2020]:
        reference_url = CENSUS_REFERNCE_URL.format(
            state_fips=state_fips, place_id=place_id, year=year
        )
        if year == 2020:
            reference_url += ".P2"
        elif year == 2010:
            reference_url += ".P2"
        elif year == 2000:
            reference_url += ".PL002"
        else:
            raise ValueError(f"Year {year} not accepted")
        ref_specs = f"<ref name=datacensus{year}p2>{{{{cite web|url={reference_url}|publisher=US Census Bureau|title={year}: DEC Redistricting Data (PL 94-171)}}}}</ref>"
        df = df.rename(columns={f"percent_{year}": f"{year}{ref_specs}"})
    return df


def get_races(year: int, state_fip: str, place_id: str) -> pd.DataFrame:
    print(f"Calling Census data for {year=}")
    c = Census(API_KEY)
    column_name = f"count_{year}"
    total_name = f"total_{year}"
    percent_name = f"percent_{year}"
    # 2010, 2020: DECENNIALPL2010.P2, DECENNIALPL2020.P2
    # 2000: DECENNIALPL2000.PL002

    if year == 2020:
        vars = P2_2020
    elif year == 2010:
        vars = P2_2010
    elif year == 2000:
        vars = P2_2000
    else:
        raise ValueError(f"Year {year} not accepted")

    total_id = [k for k, v in vars.items() if v == "total"][0]
    result = c.pl.state_place(
        fields=list(vars.keys()), state_fips=state_fip, place=place_id, year=year
    )
    result[0].pop("state")
    result[0].pop("place")
    total = result[0].pop(total_id)
    df = pd.DataFrame(result).rename(columns=vars).T
    df[total_name] = total
    df = df.rename(columns={0: column_name})
    df[[total_name, column_name]] = df[[total_name, column_name]].astype(float)
    df[percent_name] = df[column_name].div(df[total_name])
    return df


def main(args: dict) -> None:
    print(f"main started with {args=}")
    place_name = args.place_name if "args" in locals() else "Los Angeles"
    state_abbr = args.state_abbr if "args" in locals() else "CA"

    c = Census(API_KEY)

    state_fip = states.lookup(state_abbr).fips

    place_list = c.pl.state_place("NAME", state_fip, "*")
    places = [x for x in place_list if place_name.lower() in x["NAME"].lower()]
    if len(places) == 1:
        place_id = places[0]["place"]
        print(f"found place: {places}")
    else:
        print(
            f'error: more than 1 place returned {[place["NAME"] for place in places]}'
        )
        exit

    df20 = get_races(2020, state_fip, place_id)
    df10 = get_races(2010, state_fip, place_id)
    df00 = get_races(2000, state_fip, place_id)
    df = pd.concat([df00, df10, df20], axis=1)
    df = df.sort_values("percent_2020", ascending=False)

    sdf = df[[x for x in df.columns if "percent" in x]]
    sdf = (sdf * 100).round(2).astype(str) + "%"
    sdf = append_citation_to_columns(sdf, state_fips=state_fip, place_id=place_id)

    table = df_to_wikitable(
        sdf, index_name="Racial and ethnic composition", caption="Race and Ethnicity"
    )
    print("------COPY BELOW------\n")
    print(table)


def manage_cli_args() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--state-abbr",
        action="store",
        help="State abbreviation like: AL or NY",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--place-name",
        action="store",
        help="Single name of Census Designated Place like New York",
        required=True,
    )

    args, leftovers = parser.parse_known_args()
    return args


if __name__ == "__main__":
    args = manage_cli_args()
    main(args)
