
import pandas as pd
import requests
from io import StringIO
from pathlib import Path

url = "https://cuse.com/sports/womens-lacrosse/stats/2015"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

tables = pd.read_html(StringIO(response.text))

output_folder = Path("all_tables")
output_folder.mkdir(exist_ok=True)

for index, df in enumerate(tables, start=1):
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

    print("\nTable:", index)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head(2))