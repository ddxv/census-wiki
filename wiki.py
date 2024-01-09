"""Create wiki formatted tables."""
import pandas as pd

from config import (
    ACS_ESTIMATE_REFERENCE_URL,
    CENSUS_GOV_2020_REFRENCE_URL,
    ESTIMATE_YEAR,
    LATEST_DECENNIAL_CENSUS_YEAR,
)


def df_to_uscensus(
    pop_df: pd.DataFrame,
    state_fips: str,
    place_id: str,
    estimate: str,
    hist_reference: str,
) -> str:
    """Create the string version of a Wikitable with US Census references."""
    reference_url = CENSUS_GOV_2020_REFRENCE_URL.format(
        state_fips=state_fips,
        place_id=place_id,
    )
    estimate_reference_url = ACS_ESTIMATE_REFERENCE_URL.format(
        state_fips=state_fips,
        place_id=place_id,
        estimate_year=ESTIMATE_YEAR,
    )
    table = "{{US Census population\n"
    for i, x in pop_df.iterrows():
        row = f"|{i}= {x[0]}\n"
        table += row
    if estimate:
        table += f"|estyear={ESTIMATE_YEAR}\n|estimate={estimate}\n"
        table += f'|estref=<ref name="acs{ESTIMATE_YEAR}est">{{{{cite web|url={estimate_reference_url}|title=ACS Survey Population Estimate {ESTIMATE_YEAR}}}}}</ref>\n'
    footnote = f'|footnote=US Census<ref name="DecennialCensus{LATEST_DECENNIAL_CENSUS_YEAR}">{{{{cite web|url={reference_url}|title=Census of Population and Housing|publisher=Census.gov}}}}</ref>'
    if hist_reference:
        footnote += hist_reference
    table += footnote
    table += "\n}}"
    return table


def df_to_wikitable(
    df: pd.DataFrame,
    index_name: str,
    caption: str | None = None,
) -> str:
    """Create the string version of a Wikitable."""
    table = '{| class="wikitable sortable collapsible" style="font-size: 90%;"'
    if caption:
        table += f"\n|+ {caption}\n"
    columns = f"! {index_name}\n" + "! " + "\n! ".join(df.columns)
    table += columns
    # table += "\n|-"
    for i, x in df.iterrows():
        table += "\n|-"
        row_header = "\n! " + i
        values = "| " + "\n| ".join(x.to_numpy().astype(str))
        # row = row_header + "\n" + values + "\n|-"
        row = row_header + "\n" + values
        table += row
    table += "\n|}"
    return table
