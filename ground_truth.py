
import pandas as pd

file_path = "syracuse_womens_lacrosse_2015_players.csv"

df = pd.read_csv(file_path)

# Separate player rows from summary rows
players = df[~df["Player"].isin(["Total", "Opponents"])].copy()

# Split games played and games started
players[["gp", "gs"]] = (
    players["gp - gs"]
    .str.split("-", expand=True)
    .astype(int)
)

print("=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print("Total CSV rows:", len(df))
print("Player-stat rows:", len(players))
print("Unique player names:", players["Player"].nunique())

print("\nDuplicate player names:")
duplicates = players[
    players.duplicated(subset=["Player"], keep=False)
]

if duplicates.empty:
    print("No duplicates")
else:
    print(duplicates[["#", "Player", "gp - gs"]].to_string(index=False))

print("\n" + "=" * 50)
print("GROUND-TRUTH STATISTICS")
print("=" * 50)

# Most goals
most_goals = players.loc[players["g"].idxmax()]
print(
    "Most goals:",
    most_goals["Player"],
    "-",
    most_goals["g"]
)

# Most assists
most_assists = players.loc[players["A"].idxmax()]
print(
    "Most assists:",
    most_assists["Player"],
    "-",
    most_assists["A"]
)

# Most points, including ties
highest_points = players["pts"].max()
points_leaders = players[players["pts"] == highest_points]

print("\nMost points:")
for _, player in points_leaders.iterrows():
    print(player["Player"], "-", player["pts"])

# Top three goal scorers
print("\nTop three goal scorers:")
print(
    players.nlargest(3, "g")[["Player", "g"]]
    .to_string(index=False)
)

# Team totals
print("\nTotal player goals:", players["g"].sum())
print("Total player assists:", players["A"].sum())
print("Total player points:", players["pts"].sum())

# Average goals
print(
    "Average goals per player-stat row:",
    round(players["g"].mean(), 2)
)

# Ground balls
most_ground_balls = players.loc[players["GB"].idxmax()]
print(
    "\nMost ground balls:",
    most_ground_balls["Player"],
    "-",
    most_ground_balls["GB"]
)

# Caused turnovers
most_caused_turnovers = players.loc[players["ct"].idxmax()]
print(
    "Most caused turnovers:",
    most_caused_turnovers["Player"],
    "-",
    most_caused_turnovers["ct"]
)

# Draw controls
most_draw_controls = players.loc[players["dc"].idxmax()]
print(
    "Most draw controls:",
    most_draw_controls["Player"],
    "-",
    most_draw_controls["dc"]
)

# Shooting percentage with minimum 10 shots
eligible_shooters = players[players["sh"] >= 10]

best_shooter = eligible_shooters.loc[
    eligible_shooters["sh%"].idxmax()
]

print(
    "Best shooting percentage, minimum 10 shots:",
    best_shooter["Player"],
    "-",
    round(best_shooter["sh%"] * 100, 1),
    "%"
)

print("\nPlayers appearing in all 24 games:")
print(
    players[players["gp"] == 24][["Player", "gp"]]
    .to_string(index=False)
)