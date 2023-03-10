import tomllib

api_key_location = "api_key.toml"

CENSUS_REFERNCE_URL = "https://data.census.gov/table?g=1600000US{state_fips}{place_id}&y={year}&d=DEC+Redistricting+Data+(PL+94-171)&tid=DECENNIALPL{year}"

CDP_REFERENCE_URL_BASIC = (
    "https://data.census.gov/table?g=1600000US{state_fips}{place_id}&y={year}"
)

POP_VAR_NAMES = {"P1_001N": "population"}

with open(api_key_location, "rb") as f:
    data = tomllib.load(f)
    API_KEY = data["key"]
