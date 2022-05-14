import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@st.cache
def get_data():
    return pd.read_csv('kpop_idols.csv')


df = get_data()


country = st.selectbox('Country', df['Country'].value_counts().iloc[:5].index)


df_selection1 = df[lambda x: x['Country'] == country]
df_selection1


group = st.selectbox('Group', df['Group'].value_counts().index)
df_selection2 = df[lambda x: x['Group'] == group]
df_selection2




