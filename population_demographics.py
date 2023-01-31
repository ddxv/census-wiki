from wiki import df_to_wikitable, df_to_uscensus
from config import API_KEY, POP_VAR_NAMES
from census import Census
import pandas as pd
from us import states
import requests
from config import CENSUS_REFERNCE_URL


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


def open_args(args: dict) -> tuple[str, str]:
    place_name = args.place_name if "args" in locals() else "Los Angeles"
    state_abbr = args.state_abbr if "args" in locals() else "CA"
    if not place_name:
        raise ValueError(f"Place name (-p) must be included. eg: 'Los Angeles'")
    if not state_abbr:
        raise ValueError(f"State abbr (-s) must be included. eg: CA")
    return place_name, state_abbr


def get_historical_pop(state_abbr, places: list, place_name: str):
    if state_abbr != "CA":
        return pd.DataFrame(), ""
    df = pd.read_excel("data/calhist2.xls", skiprows=6)
    match_based_on_user = df["Place/Town/City"].str.lower() == place_name.lower()
    match_based_on_cdp = df["Place/Town/City"].str.lower() == places[0][
        "NAME"
    ].lower().replace(" cdp", "")
    df = df[match_based_on_cdp | match_based_on_user]
    df = df.dropna(axis=1)
    if df.shape[0] == 1:
        print(f"found historical census records {df=}")
    else:
        print(f"found too many historical census records {df=} skipping")
        df = pd.DataFrame()
    df = (
        df.drop(["County", "Place/Town/City"], axis=1)
        .reset_index(drop=True)
        .T.rename(columns={0: "Population"})
    )
    df["Population"] = df["Population"].astype(int).astype(str)
    reference = ' U.S Census 1880-1980,<ref name="1860Census">{{cite web|url=https://dof.ca.gov/reports/demographic-reports/|title=Population Totals by Township and Place for California Counties: 1860 to 1950|publisher=dof.ca.gov}}</ref>'
    return df, reference


def get_pop2021(state_fips: str, place_id: str) -> pd.DataFrame:
    print(f"Calling Census data for year=2021")
    response = requests.get(
        f"https://api.census.gov/data/2021/acs/acs5?get=NAME,B01001_001E&for=place:{place_id}&in=state:{state_fips}&key={API_KEY}"
    )
    df = pd.DataFrame(response.json()[1:], columns=response.json()[0])
    df["Year"] = 2021
    df = df.rename(columns={"B01001_001E": "Population"})
    return df


def make_demographic_tables(args):
    place_name, state_abbr = open_args(args)

    c = Census(API_KEY)

    state_fips = states.lookup(state_abbr).fips

    place_list = c.pl.state_place("NAME", state_fips, "*")
    places = [x for x in place_list if place_name.lower() in x["NAME"].lower()]
    if len(places) == 1:
        place_id = places[0]["place"]
        print(f"found place: {places}")
    else:
        raise ValueError(
            f'Place needs to be more specific. Places matched {[place["NAME"] for place in places]}'
        )

    df21 = get_pop2021(state_fips, place_id)
    df21 = df21.set_index("Year").drop(["state", "place", "NAME"], axis=1)
    acs21_estimate = df21.values[0][0]
    df20 = get_races(2020, state_fips, place_id)
    df10 = get_races(2010, state_fips, place_id)
    df00 = get_races(2000, state_fips, place_id)
    histdf, hist_reference = get_historical_pop(state_abbr, places, place_name)
    dfs = [df00, df10, df20]
    df = pd.concat(dfs, axis=1)
    df = df.sort_values("percent_2020", ascending=False)

    pop_df = (
        df[["total_2000", "total_2010", "total_2020"]]
        .reset_index(drop=True)
        .T[0]
        .reset_index()
        .rename(columns={0: "Population", "index": "Year"})
    )
    pop_df["Year"] = pop_df["Year"].str.replace("total_", "")
    pop_df["Population"] = pop_df["Population"].astype(int).astype(str)
    pop_df = pop_df.set_index("Year")
    if not histdf.empty:
        pop_df = pd.concat([histdf, pop_df])

    pop_table = df_to_uscensus(
        pop_df,
        state_fips=state_fips,
        place_id=place_id,
        year=2020,
        estimate=acs21_estimate,
        estimate_year=2021,
        hist_reference=hist_reference,
    )

    sdf = df[[x for x in df.columns if "percent" in x]]
    sdf = (sdf * 100).round(2).astype(str) + "%"
    sdf = append_citation_to_columns(sdf, state_fips=state_fips, place_id=place_id)

    table = df_to_wikitable(
        sdf, index_name="Racial and ethnic composition", caption="Race and Ethnicity"
    )
    return table, pop_table


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
