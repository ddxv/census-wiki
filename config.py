"""Editable configs."""

import tomllib

api_key_location = "api_key.toml"


CENSUS_GOV_2020_REFRENCE_URL = (
    "https://data.census.gov/table/DECENNIALPL2020.P1?g=160XX00US{state_fips}{place_id}"
)

ACS_ESTIMATE_REFERENCE_URL = (
    "https://data.census.gov/table?g=1600000US{state_fips}{place_id}&y={estimate_year}"
)

POP_VAR_NAMES = {"P1_001N": "population"}


CENSUS_2000 = 2000
CENSUS_2010 = 2010
CENSUS_2020 = 2020

LATEST_DECENNIAL_CENSUS_YEAR = CENSUS_2020

# This is used for ACS yearly estimates. Usually available end of year for preceeding year.
ESTIMATE_YEAR = 2022


with open(api_key_location, "rb") as f:
    data = tomllib.load(f)
    API_KEY = data["key"]
