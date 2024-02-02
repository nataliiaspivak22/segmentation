"""
The page with features' distributions
"""

import numpy as np
import pandas as pd

import streamlit as st
import plotly.express as px

from typing import (
    List,
    Dict, 
    Any
)

from define_objects import (
    df,
    CATEGORICAL_COLS,
    PALETTE 
)


# add selection of a number of clusters (k=2, k=3)
st.sidebar.selectbox(
    label="Number of clusters", 
    options=[2, 3], 
    index=[2, 3].index(st.session_state.get('n_clusters') or 2), 
    key="n_clusters"
)

# add multiselection as a search field for features (to plot their distributions)

################################################################################################
# TODO: Add text 'Choose a feature' as a default hint for user in a `st.multiselect` method
# Hint: Use a `placeholder` parameter
################################################################################################
# Expected solution: st.multiselect('Search', options=df.columns, key='feature', help=None, placeholder="Choose a feature")

st.multiselect(
    'Search', options=df.columns, 
    key='feature', help=None, 
)

# function to plot distribution with caching from sreamlit
@st.cache_data(ttl=3600)
def display_distribution(data: pd.DataFrame, 
                         features: List[str], 
                         cluster_col: str, 
                         categorical_cols: List[str], 
                         pallete: Dict[str, Any]) -> None:
    """
    Plot distributions of the list of input features based on the input dataframe
    If a column is within list of categorical columns -> normalized stacked barplot is created
    Otherwise -> a boxplot is shown.
    Plots are colored by cluster

    :param features: list of features to plot
    :param cluster_col: name of a column with clusters
    :param categorical_cols: list of columns, which are supposed to be categorical
    """
    for feature_name in features:
        if feature_name not in categorical_cols:
            f = px.box(
                data, x=feature_name, y=cluster_col, color=cluster_col, 
                orientation="h", color_discrete_map=pallete,
                title=f"{feature_name} by cluster",
                template="simple_white",
                labels={cluster_col: "Cluster No."}
            )
            st.plotly_chart(f)
        elif feature_name in categorical_cols:
            f = px.bar(
                data.groupby(cluster_col, sort=True)[feature_name]\
                    .value_counts(normalize=True)\
                    .reset_index(name="n")\
                    .sort_values([cluster_col, feature_name]), 
                x="n", y=cluster_col, color=feature_name, 
                orientation="h", 
                title=f"{feature_name} by cluster",
                labels={cluster_col: "Cluster No.", "n": "%"}
            )
            f.update_layout(yaxis=dict(tickmode = 'array', tickvals=np.sort(df[cluster_col].unique())))
            st.plotly_chart(f)

# create a container with plots of distributions of selected features
with st.container():
    if st.session_state.get('feature'):
        display_distribution(
            data=df, features=st.session_state.feature, 
            cluster_col=f'k={st.session_state.n_clusters}', 
            pallete=PALETTE[st.session_state.n_clusters],
            categorical_cols=CATEGORICAL_COLS
        )
