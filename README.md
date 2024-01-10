# Pull US Census Data and Transform to Wikipedia Tables

## Install

`python3 -m venv .virtualenv/` Create Python Virtual Environment
`source .virtualenv/bin/activate` activate virtual environment
`pip install -r requirements.txt` Install Requirements

## Run

`python main.py -s CA -p 'Los Angeles city'`

### CLIs

- `-s` required: State abbreviation
- `-p` requied: Place name, must be exact, will output list of examples. Since `Los Angeles` matches mutliple place names, it will prompt you to choose `Los Angeles city` or `Los Angeles county`

## Outputs

### 2000, 2010, 2020 & 202x estimate

Text of example:

```Wiki
{{US Census population
|2000= 3694820
|2010= 3792621
|2020= 3898747
|estyear=2022
|estimate=3881041
|estref=<ref name="acs2022est">{{cite web|url=https://data.census.gov/table?g=1600000US0644000&y=2022|title=ACS Survey Population Estimate 2022}}</ref>
|footnote=US Census<ref name="DecennialCensus2020">{{cite web|url=https://data.census.gov/table/DECENNIALPL2020?g=160XX00US0644000|title=Census of Population and Housing|publisher=Census.gov}}</ref>
```

### Race & Ethnicities table

A wikitext table formatted for copy-paste to wikipedia

```Wiki
 {| class="wikitable sortable collapsible" style="font-size: 90%;"   
|+ Race and Ethnicity
! Racial and ethnic composition
! 2000<ref name=datacensus2000p2>{{cite web|url=https://data.census.gov/table?g=1600000US0644000&y=2000&d=DEC+Redistricting+Data+(PL+94-171)&tid=DECENNIALPL2000.PL002|publisher=US Census Bureau|title=2000: DEC Redistricting Data (PL 94-171)}}</ref>
! 2010<ref name=datacensus2010p2>{{cite web|url=https://data.census.gov/table?g=1600000US0644000&y=2010&d=DEC+Redistricting+Data+(PL+94-171)&tid=DECENNIALPL2010.P2|publisher=US Census Bureau|title=2010: DEC Redistricting Data (PL 94-171)}}</ref>
! 2020<ref name=datacensus2020p2>{{cite web|url=https://data.census.gov/table?g=1600000US0644000&y=2020&d=DEC+Redistricting+Data+(PL+94-171)&tid=DECENNIALPL2020.P2|publisher=US Census Bureau|title=2020: DEC Redistricting Data (PL 94-171)}}</ref>
|-
! [[Hispanic and Latino Americans|Hispanic or Latino (of any race)]]
| 46.53%
| 48.48%
| 46.94%
|-
! [[Non-Hispanic whites|White (non-Hispanic)]]
| 29.75%
| 28.66%
| 28.88%
|-
! [[Asian American|Asian (non-Hispanic)]]
| 9.87%
| 11.08%
| 11.66%
|-
! [[African American|Black or African American (non-Hispanic)]]
| 10.88%
| 9.16%
| 8.27%
|-
! [[Multiracial American|Two or more races (non-Hispanic)]]
| 2.36%
| 2.01%
| 3.28%
|-
! Other (non-Hispanic)
| 0.25%
| 0.32%
| 0.68%
|-
! [[Native Americans in the United States|Native American (non-Hispanic)]]
| 0.24%
| 0.17%
| 0.17%
|-
! [[Pacific Islander Americans|Pacific Islander (non-Hispanic)]]
| 0.12%
| 0.11%
| 0.12%
|}
```
