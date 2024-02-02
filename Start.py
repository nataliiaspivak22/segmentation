"""
The initial page of the app with
-> bar, scatter 2d/3d plots
-> metrics, tables
-> streamlit's tabs
"""
from typing import Dict

import streamlit as st
import plotly.express as px

from tools.tools import short_format
from define_objects import (
    df, 
    df_stats_by_clst, 
    df_stats_by_cat,
    PALETTE
)

######################################################################################################
# HW: If you'd like tp play with parsing arguments from the command line -- uncomment the code below
# 
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("--algo", required=True , choices=['kmeans', 'dbscan'], help="A clustering algorithm selection")
# args = parser.parse_args()
######################################################################################################
args: Dict[str, str] = dict(algo='kmeans')

# set page configuration
st.set_page_config("Segmentation", layout="wide")

# set headers
st.markdown("# Customer Personality Analysis. Q1-2024")

################################################################################################
# TODO: Add heading level 2 with the text: Wines, Fruits, Meat, Fish, Sweet, Gold.
# Hint: Level 2 heading start with 2 hashtags.
################################################################################################
# Expected solution: st.markdown("## " + ", ".join(categories) + ".")


# add selection of a number of clusters (k=2, k=3)
st.sidebar.selectbox(
    label="Number of clusters", options=[2, 3], index=0, key="n_clusters"
)

# 1. add container with overall plots:
# - total spend by category
# - SpendOnMeatProducts & SpendOnWines by cluster
# - SpendOnFishProducts & SpendOnGoldProds by cluster
# - 3d projection colored by clusters
with st.container():

    # create a separate column for each plot 
    gen_cols = st.columns(4)
    
    # -> add total spend by category to the 1st streamlit column
    with gen_cols[0]:

        ########################################################################################################
        # TODO: Add a standard streamlit bar plot with total spends by categories, with 
        #       color='#5674a5', height=300, width=450, 
        #       align it with conainer's width
        # Hint: Use st.bar_chart as a main tool and it's parameters: color, width, height, use_container_width
        ########################################################################################################
        # Expected solution: 
        # st.bar_chart(data=df_stats_by_cat, y='sum', color='#5674a5', height=300, width=450, use_container_width=True)

        ########################################################################################################
        # TODO: Compare the st.bar_chart with the one from plotly express
        ########################################################################################################

        f = px.bar(
            df_stats_by_cat, 
            y="sum",
            title="Total Spend by Category",
            text_auto='$.2s',
            color_discrete_sequence=['#5674a5'],
            labels={'index': '', 'sum': ''},
            height=300, width=450
        )
        st.plotly_chart(f)

    # -> add SpendOnMeatProducts & SpendOnWines by cluster to the 2nd streamlit column
    with gen_cols[1]:
        f = px.scatter(
            df, 
            x="%SpendOnMeatProducts",
            y="%SpendOnWines",
            color=f"k={st.session_state.n_clusters}",
            title="% Spend on Meat & Wine by cluster",
            color_discrete_map=PALETTE[st.session_state.n_clusters],
            height=300, width=450
        )
        st.plotly_chart(f)        

    # -> add SpendOnMeatProducts & SpendOnWines by cluster to the 3d streamlit column
    with gen_cols[2]:
        f = px.scatter(
            df, 
            x="%SpendOnFishProducts",
            y="%SpendOnGoldProds",
            color=f"k={st.session_state.n_clusters}",
            title="% Spend on Fish & Gold by cluster",
            custom_data=[df[f"k={st.session_state.n_clusters}"]],
            color_discrete_map=PALETTE[st.session_state.n_clusters],
            height=300, width=450
        )
        f.update_traces(
             hovertemplate = '%Spend on Fish: %{x:.2%}' +\
                '<br>' + '%Spend on Gold: %{y:.2%}',
        )
        f.update_layout(yaxis_tickformat='.0%',xaxis_tickformat='.0%')
        st.plotly_chart(f) 

    # -> add PCA projections as 3d scatter plot colored by clustersto the 4th streamlit column
    with gen_cols[3]:
        f = px.scatter_3d(
            df, x='PCA.1', y='PCA.2', z='PCA.3',
            size=[1]*len(df), 
            size_max=7, opacity=0.5,
            color=f'k={st.session_state.n_clusters}',
            color_discrete_map=PALETTE[st.session_state.n_clusters], 
            height=300, width=320,
            template="plotly_white",
            title="3d projection of clusters"
        )
        f.update_layout(margin=dict(l=20, r=70, b=10, t=100, pad=0))                    
        st.plotly_chart(f)

# 2. add expander with clusters' charecteristics: median/top values by features, which differ from cluster to cluster

#  exract a data frame with computed statistics per cluster
df_selected_stats = df_stats_by_clst[args['algo']][f'k={st.session_state.n_clusters}']
n_features = df_selected_stats.shape[1]

with st.expander("Averages by clusters:", expanded=True):

    # create tabs to switch between metrics visualized with indicators and table-based view
    tab_1, tab_2 = st.tabs(['Metrics', 'Tables'])

    # -> fill the first tab
    with tab_1:
        # for each cluster 
        for c in range(st.session_state.n_clusters):
            # create a container for each cluster to controll metrics heights
            with st.container(height=200):

                # extract the cluster's color from pallete to make a fancy title
                cluster_color = PALETTE[st.session_state.n_clusters][str(c)]
                # make a title
                        
                ########################################################################################################
                # TODO: Add a title 'Cluster #NO_OF_A_CLUSTER'. The title should be colored by its cluster's color
                # Hint: To color text use construction: :{COLOR}[TEXT]
                ########################################################################################################
                # Expected solution: st.markdown(f":{cluster_color}[Cluster #{c}: ]")
                
                # create a column for each metric 
                # extract the metric's values by cluster and by the whole population
                # format metric to have a fancy visualization
                st_cols = st.columns(n_features, gap="small")
                for i, col_name in enumerate(df_selected_stats.columns):
                    # ---> by cluster
                    cl_value = short_format(df_selected_stats.loc[str(c), col_name])
                    cl_value_frmt = f'{cl_value:.1%}' if '%' in col_name else str(cl_value)

                    # ---> by whole population
                    over_value = short_format(df_selected_stats.loc['Overall', col_name])
                    over_value_frmt = f'{over_value:.1%}' if '%' in col_name else str(over_value)

                    # by default, streamlit displays an up/down arrow in a benchmark section
                    # this object is redundant in our case, so with html below we 'ignore it'
                    st.write(
                        """
                        <style>
                        [data-testid="stMetricDelta"] svg {
                        display: none;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    # display metrics
                    ########################################################################################################
                    # TODO: Remove coloring of a delta value from metrics method 
                    # 
                    # Hint: Change a `delta_color` parameter of a st.metric method
                    ########################################################################################################
                    # Expected solution: st_cols[i].metric(label=col_name, value=cl_value_frmt, delta=over_value_frmt, delta_color='off')
                    
    # -> fill the second tab with a table
    with tab_2:
        st.dataframe(df_selected_stats)