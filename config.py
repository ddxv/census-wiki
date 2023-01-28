import tomllib

api_key_location = "api_key.toml"

with open(api_key_location, "rb") as f:
    data = tomllib.load(f)
    API_KEY = data["key"]
