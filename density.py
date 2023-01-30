from census import Census
from config import API_KEY
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px

import requests
from io import BytesIO


ftp_file = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/place/tab20_place20_place10_natl.txt"
file = requests.get(ftp_file)

df = pd.read_csv(
    BytesIO(file.content),
    sep="|",
    dtype={"GEOID_PLACE_20": "object", "OID_PLACE_20": "object", "GEOID_PLACE_10":"object"},
)


df["geoid"] = df["GEOID_PLACE_20"]


pop_var_names = {"P1_001N": "population"}


def get_pops(year: int) -> pd.DataFrame:
    print(f"Calling Census data for {year=}")
    c = Census(API_KEY)

    var = "P1_001N"
    resp = c.pl.get(var, {"for": "place:*"})
    pop = pd.DataFrame(resp)

    pop = pop.rename(columns=pop_var_names)

    pop["geoid"] = pop["state"] + pop["place"]
    pop

    merged = pd.merge(
        df, pop, how="inner", left_on=["geoid"], right_on=["geoid"]
    )

    merged['geoid'].value_counts()

    pop[pop['geoid'] == '0107000']
    df[df['geoid'] == '0107000'][['GEOID_PLACE_20', 'OID_PLACE_20']]


    merged['geoid'].value_counts()

    response = requests.get(
        f"https://api.census.gov/data/2020/dec/pl?get=NAME,{var}&for=place&key={API_KEY}"
    )
    response.json()

    result[0].pop("state")
    result[0].pop("place")
    total = result[0].pop(total_id)
    df = pd.DataFrame(result).rename(columns=vars).T
    df[total_name] = total
    df = df.rename(columns={0: column_name})
    df[[total_name, column_name]] = df[[total_name, column_name]].astype(float)
    df[percent_name] = df[column_name].div(df[total_name])
    return df


def make_race_demographic_table(args):
    place_name, state_abbr = open_args(args)

    c = Census(API_KEY)

    state_fip = states.lookup(state_abbr).fips

    place_list = c.pl.state_place("NAME", state_fip, "*")
    places = [x for x in place_list if place_name.lower() in x["NAME"].lower()]
    if len(places) == 1:
        place_id = places[0]["place"]
        print(f"found place: {places}")
    else:
        raise ValueError(
            f'Place needs to be more specific. Places matched {[place["NAME"] for place in places]}'
        )

    df20 = get_races(2020, state_fip, place_id)
    df10 = get_races(2010, state_fip, place_id)
    df00 = get_races(2000, state_fip, place_id)
    df = pd.concat([df00, df10, df20], axis=1)
