import pandas as pd
import requests
from io import StringIO
from pathlib import Path

url = "https://cuse.com/sports/womens-lacrosse/stats/2015"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Download the webpage
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

# Extract all HTML tables
tables = pd.read_html(StringIO(response.text))

print(f"Number of tables found: {len(tables)}")

# Create output folder
output_folder = Path("cuse_2015_csv")
output_folder.mkdir(exist_ok=True)

# Save every table separately
for index, df in enumerate(tables, start=1):

    # Flatten multi-level column names, if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join(
                str(value).strip()
                for value in column
                if str(value) != "nan"
            )
            for column in df.columns
        ]

    filename = output_folder / f"table_{index}.csv"
    df.to_csv(filename, index=False)

    print(f"Saved {filename} — {df.shape[0]} rows")

for index, df in enumerate(tables, start=1):
        print("\nTABLE", index)
        print(df.columns.tolist())
        print(df.head())

player_stats = None

for df in tables:
    columns = " ".join(str(column).lower() for column in df.columns)

    if "player" in columns and "pts" in columns:
        player_stats = df.copy()
        break

if player_stats is None:
    raise ValueError("Player statistics table was not found.")

if isinstance(player_stats.columns, pd.MultiIndex):
    player_stats.columns = [
        "_".join(
            str(value).strip()
            for value in column
            if str(value) != "nan"
        )
        for column in player_stats.columns
    ]

player_stats.to_csv("syracuse_womens_lacrosse_2015_players.csv", index=False)

print(player_stats.head())


