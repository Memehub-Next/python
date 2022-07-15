from statistics import stdev
from typing import Any, cast

import pandas as pd
from numpy import e, log
from pandas.core.frame import DataFrame


def score_df(scoring: DataFrame):
    top_1percent = scoring[scoring["upvotes"] > scoring["upvotes"].quantile(0.99)]
    bottom_99 = scoring[scoring["upvotes"] < scoring["upvotes"].quantile(0.99)]
    authors = list(set(cast(list[str], list(top_1percent["username"]))))
    lowest_upvotes_in_top = cast(int, top_1percent["upvotes"].min())
    num_memes_in_bottom: dict[str, int] = bottom_99.groupby("username").apply(len).sort_values(ascending=False)
    num_memes_in_top: dict[str, int] = top_1percent.groupby("username").apply(len).sort_values(ascending=False)
    highest_upvotes = cast(dict[str, int], top_1percent.groupby("username")["upvotes"].max())
    lowest_upvote_ratio: dict[str, float] = top_1percent.groupby("username")["upvote_ratio"].apply(min).sort_values(ascending=False)

    num_memes_in_bottom_filled: list[int] = []
    for author in authors:
        try:
            num_memes_in_bottom_filled.append(num_memes_in_bottom[author])
        except Exception:
            num_memes_in_bottom_filled.append(0)

    scores_dict: dict[str, Any] = {}
    for author in authors:
        try:
            inv_spammer_index = num_memes_in_top[author] / (num_memes_in_bottom[author] + 1)
            spammer_index = num_memes_in_bottom[author] / num_memes_in_top[author]
        except Exception:
            inv_spammer_index = num_memes_in_top[author]
            spammer_index = 0
        highest_upvotes_score: float = log(e + (highest_upvotes[author] / lowest_upvotes_in_top))
        lowest_ratio = lowest_upvote_ratio[author]
        scores_dict[author] = {"spammer_index": spammer_index,
                               "highest_upvotes_score": highest_upvotes_score,
                               "lowest_ratio": lowest_ratio,
                               "score": inv_spammer_index * highest_upvotes_score * lowest_ratio}
    raw_scores: list[float] = [scores_dict[author]["score"] for author in authors]
    final_scores: list[float] = 50 / (2.2 * stdev(log(raw_scores))) * log(raw_scores) + 50

    return (
        pd.DataFrame({"username": authors,
                      "final_score": final_scores,
                      "raw_score": raw_scores,
                      "num_in_bottom": num_memes_in_bottom_filled,
                      "num_in_top": [num_memes_in_top[author] for author in authors],
                      "shitposter_index": [scores_dict[author]["spammer_index"] for author in authors],
                      "highest_upvotes": [highest_upvotes[author] for author in authors],
                      "hu_score": [scores_dict[author]["highest_upvotes_score"] for author in authors],
                      "lowest_ratio": [scores_dict[author]["lowest_ratio"] for author in authors]})
        .sort_values("final_score", ascending=False)
        .reset_index(drop=True)
        .round(decimals=2)
    )


score_columns = ["username",
                 "final_score",
                 "raw_score",
                 "num_in_bottom",
                 "num_in_top",
                 "shitposter_index",
                 "highest_upvotes",
                 "hu_score",
                 "lowest_ratio"]


def score_kwargs_gen(df: DataFrame):
    for _, row in df.iterrows():
        yield {column: row[column] for column in score_columns}
