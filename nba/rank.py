import pandas as pd

"""
Values using standard 8 cats.
Punting turnovers of course.
"""

df = pd.read_csv("projections/projections.csv")

STATS = [
    "points",
    "threes",
    "rebounds",
    "assists",
    "blocks",
    "steals"
]

RANK_STATS = [
    "points_z_score",
    "threes_z_score",
    "rebounds_z_score",
    "assists_z_score",
    "blocks_z_score",
    "steals_z_score",
    "field_goal_z_score",
    "free_throw_z_score"
]

# calculate points and rebounds
df["points"] = ( (df["field_goals"] - df["threes"]) * 2 ) + ( df["threes"] * 3 ) + ( df["free_throws"] * 1 )
df["rebounds"] = df["offensive_rebounds"] + df["defensive_rebounds"]

# calculate percentage impact
avg_fg_percentage = df["field_goals"].sum() / df["field_goals_attempted"].sum()
avg_ft_percentage = df["free_throws"].sum() / df["free_throws_attempted"].sum()
df["fg_impact"] = ( (df["field_goals"] / df["field_goals_attempted"]) - avg_fg_percentage ) * df["field_goals_attempted"]
df["ft_impact"] = ( (df["free_throws"] / df["free_throws_attempted"]) - avg_ft_percentage ) * df["free_throws_attempted"]

# calculate per game counting stats and z-scores for them
for column in STATS:
    per_game_stat = column + "_per_game"
    df[per_game_stat] = df[column] / df["games"]
    df[column + "_z_score"] = (df[per_game_stat] - df[per_game_stat].mean()) / df[per_game_stat].std()

# calculate z-scores for percentage impact stats
df["field_goal_z_score"] = (df["fg_impact"] - df["fg_impact"].mean()) / df["fg_impact"].std()
df["free_throw_z_score"] = (df["ft_impact"] - df["ft_impact"].mean()) / df["ft_impact"].std()

# aggregate the z-scores
df["value"] = df[RANK_STATS].mean(axis=1)
df = df.sort_values(by=["value"], ascending=False)

df.to_csv('output.csv')
