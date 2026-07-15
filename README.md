

# Task 05: Descriptive Statistics and Large Language Models

## Project Description

This project evaluates how accurately a large language model can answer
factual and judgment-oriented questions about the 2015 Syracuse University
women's lacrosse statistics.

Python was used to calculate verified ground-truth results. The same
questions were then provided to an LLM, and its answers were compared
against the Python results.

## Dataset

The project uses publicly available 2015 Syracuse University women's
lacrosse statistics.

Source:
https://cuse.com/sports/womens-lacrosse/stats/2015

The original dataset is not included in this repository. Download the data
from the source page and save it locally as:
syracuse_womens_lacrosse_2015_players.csv

## Phase A: Ground Truth and Baseline LLM Evaluation

In Phase A, I tested whether ChatGPT GPT-5.6 Thinking could answer factual questions directly from the uploaded CSV. I asked the model to identify the number of player-stat rows and the leaders in goals, assists, total points, ground balls, caused turnovers, draw controls, and shooting percentage. I also asked it to report the top three goal scorers and identify duplicate player names.

The Python analysis showed that the dataset contained 44 player-stat rows and 43 unique players. Kayla Treanor led the team with 60 goals, while Halle Majorana recorded the most assists with 36. Treanor and Majorana tied for the highest total points with 91 each. The three leading goal scorers were Treanor with 60, Majorana with 55, and Riley Donahue with 28. Kelsey Richardson led the team with 53 ground balls, Mallory Vehar caused the most turnovers with 27, and Kailah Kempney recorded the most draw controls with 186.

The language model correctly reported all these statistical results. It also correctly detected that Madeleine Walton appeared twice. However, it incorrectly described the uploaded file as game-level data even though it contained cumulative player-level statistics. This demonstrated that a model may calculate the requested values correctly while still misunderstanding or incorrectly describing the structure of the dataset.

The shooting-percentage question also exposed a weakness in my original ground-truth script. The script used idxmax(), which returned only the first player with the maximum value. It therefore identified Riley Donahue as the only leader. The language model reported a tie between Donahue and Kelly Cross at 51.9%. A manual check showed that Donahue scored 28 goals on 54 shots and Cross scored 14 goals on 27 shots. Both ratios equal approximately 51.85% and are displayed as 51.9% in the dataset. The model was correct, while the original Python validation method failed to preserve ties.

This was an important finding because it showed that ground truth is only reliable when the validation code correctly handles edge cases. I revised the evaluation approach to identify every row equal to the maximum value instead of returning only the first occurrence.

## Phase B: Derived Metrics and Judgment Questions

Phase B moved beyond direct lookups and required a measurable definition for the qualitative concept of a “game changer.” Instead of allowing the model to create its own interpretation, I explicitly defined a Game Changer Score.

Only players who appeared in at least 10 games were eligible. I first calculated five statistics on a per-game basis:

Goals per game
Assists per game
Ground balls per game
Caused turnovers per game
Draw controls per game

I used per-game values so that players with different numbers of appearances could be compared more fairly. Because these statistics use very different numerical scales, I applied min-max normalization to convert each metric to a value between zero and one.

The final score used the following weights:

Goals per game: 40%
Assists per game: 20%
Ground balls per game: 15%
Caused turnovers per game: 15%
Draw controls per game: 10%

Goals and assists received the highest weights because direct scoring production is a major part of winning lacrosse games. Ground balls, caused turnovers, and draw controls were also included to represent defensive activity and possession.

My independent Python calculation produced the following top-five ranking:

Rank	Player	Game Changer Score
1	Kayla Treanor	76.07
2	Halle Majorana	62.76
3	Kelly Cross	43.11
4	Kailah Kempney	42.64
5	Riley Donahue	37.90

I then uploaded the same CSV to the language model and supplied the complete eligibility rule, normalization method, metric weights, and instructions to use only the uploaded data. I also asked the model to show its calculations and avoid substituting its own definition. The model reproduced the same top-five ranking and scores as the Python analysis.

The Phase B result showed that prompt specificity had a major effect on analytical reliability. A vague question such as “Who is the game changer?” would allow the model to choose its own criteria. By explicitly defining eligibility, per-game calculations, normalization, weights, and output requirements, I converted the judgment question into a reproducible analytical task.

## Coaching Recommendation

Within the limits of this player-level dataset, I recommend that the team place slightly more emphasis on developing its defense and possession play while maintaining its existing offensive strengths.

The offense was already led by two highly productive players. Kayla Treanor recorded 60 goals and 31 assists, while Halle Majorana recorded 55 goals and 36 assists. Both finished with 91 total points and ranked first and second in the Game Changer Score. These results indicate that the team already had established high-level offensive production.

The defensive and possession statistics were more distributed across specialized contributors. Kelsey Richardson led the team with 53 ground balls, Mallory Vehar caused 27 turnovers, and Kailah Kempney recorded 186 draw controls. Strengthening the team’s defensive consistency and ability to gain or retain possession could create more offensive opportunities while reducing opponents’ opportunities.

Kelly Cross should receive focused development as a potential future game changer. She ranked third in the Game Changer Score despite appearing in only 11 games. She averaged approximately 1.27 goals, 0.55 assists, 1.00 ground ball, 0.55 caused turnovers, and 1.09 draw controls per game. This balanced contribution across scoring, defense, and possession suggests that she could have a larger impact with additional playing time, coaching, and role development. Treanor and Majorana were already established game changers, while Cross represented a player with meaningful growth potential.

This recommendation must be interpreted cautiously. The dataset contains cumulative player statistics but does not include minutes played, player positions, injuries, opponent strength, detailed game situations, or the relationship between individual performances and game outcomes. The Game Changer Score also depends on subjective weights that favor offense. Min-max normalization is sensitive to extreme values, particularly Kempney’s unusually high draw-control total. Therefore, this analysis identifies promising patterns but cannot prove that defensive development alone would cause the team to win two additional games.

## Overall Reflection

The experiment showed that a language model can be effective when working with a small, structured dataset, especially when the prompt supplies exact definitions and requires visible calculations. In Phase A, the model accurately answered factual questions but incorrectly characterized the dataset. It also helped reveal a flaw in my own Python validation code by correctly preserving a statistical tie that idxmax() had hidden.

In Phase B, the model followed a custom metric successfully because the prompt clearly defined the eligible population, formulas, normalization method, weights, and expected output. The result was much more reliable than asking the model to make an undefined judgment.

Based on this experiment, I would trust an LLM to assist with data exploration, calculations, explanations, and initial recommendations when the data and instructions are clearly specified. However, I would not accept its output without validation. Dataset interpretation, duplicate handling, ties, metric assumptions, and open-ended recommendations still require human review. The most useful role for the LLM was not replacing the analytical process, but supporting a process in which its conclusions could be reproduced and checked independently.
