"""
A module, which defines main constants and loads data
"""

import os
from  typing import (
    List,
    Dict,
    Any
)
import pandas as pd


# load data
# - define path to it
PROJECT_PATH: str = os.getcwd()
DATA_PATH: str = os.path.join(PROJECT_PATH, "data")

# - read it
df: pd.DataFrame = pd.read_pickle(os.path.join(DATA_PATH, 'clusters.pckl'))

# list columns' names from the dataset 
# - which are categorical
CATEGORICAL_COLS: List[str] = ['Kidhome', 'Education']

# - which represent products' categories
PRODUCTS_CATEGORIES: List[str] = ['Wines', 'Fruits', 'Meat', 'Fish', 'Sweet', 'Gold']

# define clusters' colors in a way, that clusters with 
# - a lower average spend are redish 
# - a larger average spend are greenish
PALETTE: Dict[int, Any] = {
    2: dict(
        zip(
            df.groupby(["k=2"], sort=False).TotalSpends.median().sort_values().index, 
            ("red", "green")
        )
    ),
    3: dict(
        zip(
            df.groupby(["k=3"], sort=False).TotalSpends.median().sort_values().index, 
            ("red", "orange", "green")
        )
    )
}

# Compute mean and std of spends by each product category in the format: 
# -------------------------------------------------------------------------
#               Wines        Fruits           Meat          Fish         Sweet          Gold
# sum   675093.000000  58219.000000  364513.000000  83253.000000  59818.000000  97146.000000
# mean     306.164626     26.403175     165.312018     37.756463     27.128345     44.057143
df_stats_by_cat: pd.DataFrame = df[PRODUCTS_CATEGORIES].agg(['sum', 'mean']).T

# read saved averages/top values by columns by clusters and save them into a dictionary
df_stats_by_clst: Dict[str, Dict[str, pd.DataFrame]] = dict(kmeans=dict())
df_stats_by_clst['kmeans']['k=2'] = pd.read_pickle(os.path.join(DATA_PATH, 'k_means_keq2.pckl'))
df_stats_by_clst['kmeans']['k=3'] = pd.read_pickle(os.path.join(DATA_PATH, 'k_means_keq3.pckl'))
