import pandas as pd

# Load player statistics
df = pd.read_csv("syracuse_womens_lacrosse_2015_players.csv")

# Remove team summary rows
players = df[
    ~df["Player"].isin(["Total", "Opponents"])
].copy()

# Separate games played and games started
players[["gp", "gs"]] = (
    players["gp - gs"]
    .str.split("-", expand=True)
    .astype(int)
)

# Ensure statistical columns are numeric
stat_columns = ["g", "A", "GB", "ct", "dc"]

for column in stat_columns:
    players[column] = pd.to_numeric(
        players[column],
        errors="coerce"
    ).fillna(0)

# Combine duplicate player-name rows
players = (
    players.groupby("Player", as_index=False)
    .agg({
        "gp": "sum",
        "g": "sum",
        "A": "sum",
        "GB": "sum",
        "ct": "sum",
        "dc": "sum"
    })
)

# Only include players who appeared in at least 10 games
eligible = players[players["gp"] >= 10].copy()

# Calculate per-game statistics
for column in stat_columns:
    eligible[f"{column}_per_game"] = (
        eligible[column] / eligible["gp"]
    )

# Normalize each per-game statistic from 0 to 1
for column in stat_columns:
    rate_column = f"{column}_per_game"
    minimum = eligible[rate_column].min()
    maximum = eligible[rate_column].max()

    if maximum == minimum:
        eligible[f"{column}_normalized"] = 0
    else:
        eligible[f"{column}_normalized"] = (
            eligible[rate_column] - minimum
        ) / (maximum - minimum)

# Calculate weighted Game Changer Score
eligible["game_changer_score"] = 100 * (
    0.40 * eligible["g_normalized"]
    + 0.20 * eligible["A_normalized"]
    + 0.15 * eligible["GB_normalized"]
    + 0.15 * eligible["ct_normalized"]
    + 0.10 * eligible["dc_normalized"]
)

# Sort players from highest to lowest
ranking = eligible.sort_values(
    "game_changer_score",
    ascending=False
)

# Display the top players
display_columns = [
    "Player",
    "gp",
    "g_per_game",
    "A_per_game",
    "GB_per_game",
    "ct_per_game",
    "dc_per_game",
    "game_changer_score"
]

print("\nGame Changer Ranking:\n")

print(
    ranking[display_columns]
    .head(10)
    .round(3)
    .to_string(index=False)
)

# Save the complete ranking
ranking[display_columns].round(3).to_csv(
    "game_changer_ranking.csv",
    index=False
)

# Print the final ground-truth answer
winner = ranking.iloc[0]

print("\nGround-truth result:")
print(
    f"{winner['Player']} has the highest Game Changer Score: "
    f"{winner['game_changer_score']:.2f}"
)