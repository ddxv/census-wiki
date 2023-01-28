import pandas as pd


def df_to_wikitable(df: pd.DataFrame, index_name: str, caption=None) -> str:
    table = f'{{| class="wikitable sortable collapsible" style="font-size: 90%;"   \n|+ {caption}\n'
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
