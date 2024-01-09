import pandas as pd

from config import CDP_REFERENCE_URL_BASIC


def df_to_uscensus(
    pop_df: pd.DataFrame,
    state_fips: str,
    place_id: str,
    year: int,
    estimate: str,
    estimate_year: int,
    hist_reference: str,
) -> str:
    reference_url = CDP_REFERENCE_URL_BASIC.format(
        state_fips=state_fips, place_id=place_id, year=year
    )
    table = "{{US Census population\n"
    for i, x in pop_df.iterrows():
        row = f"|{i}= {x[0]}\n"
        table += row
    if estimate:
        table += f"|estyear={estimate_year}\n|estimate={estimate}\n"
        table += f'|estref=<ref name="acs{estimate_year}est">{{{{cite web|url=https://data.census.gov/table?g=1600000US{state_fips}{place_id}&y={estimate_year}|title=ACS Survey Population Estimate {estimate_year}}}}}</ref>\n'
    footnote = f'|footnote=US Census<ref name="DecennialCensus{year}">{{{{cite web|url={reference_url}.P1|title=Census of Population and Housing|publisher=Census.gov}}}}</ref>'
    if hist_reference:
        footnote += hist_reference
    table += footnote
    table += "\n}}"
    return table


def df_to_wikitable(
    df: pd.DataFrame, index_name: str, caption: str | None = None
) -> str:
    table = '{| class="wikitable sortable collapsible" style="font-size: 90%;"'
    if caption:
        table += f"\n|+ {caption}\n"
    columns = f"! {index_name}\n" + "! " + "\n! ".join(df.columns)
    table += columns
    # table += "\n|-"
    for i, x in df.iterrows():
        table += "\n|-"
        row_header = "\n! " + i
        values = "| " + "\n| ".join(x.values.astype(str))
        # row = row_header + "\n" + values + "\n|-"
        row = row_header + "\n" + values
        table += row
    table += "\n|}"
    return table
