"""Density tables, but currently a work in progress."""
import pandas as pd
import requests
from census import Census

from config import API_KEY, POP_VAR_NAMES
from logger import get_logger

logger = get_logger(__name__)

ftp_file = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/place/tab20_place20_place10_natl.txt"
file = requests.get(ftp_file, timeout=5)


def get_tigerweb_area(state_fips: str) -> pd.DataFrame:
    """Get tigerweb area for size of location."""
    outfields = ["GEOID", "BASENAME", "AREALAND", "AREAWATER"]
    params = {
        "outFields": ",".join(outfields),
        #'outFields':outfields,
        "where": f"STATE='{state_fips}'",
        "returnGeometry": "false",
        "f": "json",
        "units": "esriSRUnit_Foot",
        "sqlFormat": "none",
        "featureEncoding": "esriDefault",
    }
    # TIGERWEB_CENSUS2020 = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/19/query?text=Guerneville&units=esriSRUnit_Foot&outFields=GEOID%2CAREALAND%2CAREAWATER%2CBASENAME%2CSTATE&returnGeometry=false&f=pjson'
    # response = requests.get(TIGERWEB_CENSUS2020)
    # response.json()
    tigerweb_census2020 = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/19/query"
    response = requests.get(tigerweb_census2020, params=params, timeout=2)
    myjson = response.json()
    df = pd.DataFrame(myjson["features"])
    df = pd.json_normalize(df["attributes"])
    df.columns = df.columns.str.lower()
    return df


def get_pops(year: int, state_fips: str) -> pd.DataFrame:
    """Get populations for area."""
    logger.info("Calling Census data", extra={"year": year})
    c = Census(API_KEY)

    var = "P1_001N"
    resp = c.pl.get(var, {"for": "place:*"})
    pop = pd.DataFrame(resp)

    pop = pop.rename(columns=POP_VAR_NAMES)

    pop["geoid"] = pop["state"] + pop["place"]

    state_fips = "06"

    area_df = get_tigerweb_area(state_fips=state_fips)

    merged = area_df.merge(
        pop,
        how="inner",
        left_on=["geoid"],
        right_on=["geoid"],
        validate="1:1",
    )
    merged["area_km"] = merged["arealand"] / 1000000
    merged["pop_per_km"] = merged["population"] / merged["area_km"]

    merged = merged.sort_values("pop_per_km", ascending=False)

    merged.head(20)

    merged["geoid"].value_counts()

    pop[pop["geoid"] == "0107000"]
    # df[df["geoid"] == "0107000"][["GEOID_PLACE_20", "OID_PLACE_20"]]

    merged["geoid"].value_counts()

    response = requests.get(
        f"https://api.census.gov/data/2020/dec/pl?get=NAME,{var}&for=place&key={API_KEY}",
        timeout=5,
    )
    result = response.json()

    result[0].pop("state")
    result[0].pop("place")
    # total = result[0].pop(total_id)
    # df[total_name] = total
    # df = df.rename(columns={0: column_name})
    # df[[total_name, column_name]] = df[[total_name, column_name]].astype(float)
    # df[percent_name] = df[column_name].div(df[total_name])
    return pd.DataFrame(result).rename(columns=vars).T


# def make_race_demographic_table(args: argparse.Namespace) -> None:
#     place_name, state_abbr = open_args(args)

#     c = Census(API_KEY)

#     state_fip = states.lookup(state_abbr).fips

#     place_list = c.pl.state_place("NAME", state_fip, "*")
#     places = [x for x in place_list if place_name.lower() in x["NAME"].lower()]
#     if len(places) == 1:
#         place_id = places[0]["place"]
#         print(f"found place: {places}")
#     else:
#         raise ValueError(
#             f'Place needs to be more specific. Places matched {[place["NAME"] for place in places]}'
#         )

#     df20 = get_races(2020, state_fip, place_id)
#     df10 = get_races(2010, state_fip, place_id)
#     df00 = get_races(2000, state_fip, place_id)
#     df = pd.concat([df00, df10, df20], axis=1)
