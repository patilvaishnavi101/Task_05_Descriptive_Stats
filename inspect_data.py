
import pandas as pd

file_path = "syracuse_womens_lacrosse_2015_players.csv"

df = pd.read_csv(file_path)

print("Rows and columns:", df.shape)

print("\nColumn names:")
for column in df.columns:
    print(column)

print("\nFirst five rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)