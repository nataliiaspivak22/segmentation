"""
The page with
-> ID input for search within pd.DataFame
-> comunication with the pd.DataFrame
"""
import streamlit as st

from define_objects import (
    df
)


# text input
################################################################################################
# TODO: Add text input for user's ID 
# - define label as 'ID', 
# - maximum number of input symbols as 5
# - the key to access a session state as 'ID'
# 
# Hint: Use a st.text_input method and its parameters:
# - label
# - max_chars
# - key
################################################################################################
# Expected solution: st.text_input('ID', max_chars=5, key='ID')


# display a row, which corresponds to the input user's ID 
# -> there is one in the data frame
# -> show warning otherwise
if st.session_state.get('ID'):
    user_info = df[df.ID.astype(str) == st.session_state.get('ID')]
    if not user_info.empty:
        st.table(user_info)
    else:
        st.warning(f'There is no customer with `ID`={st.session_state.get("ID")}')


# create a column for communication
df['Checked'] = False

# make a data frame editable and display it
st.data_editor(df[["ID", "Year_Birth", "Income", "k=2", "k=3", "Checked"]], num_rows="dynamic")
