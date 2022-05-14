import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


st.set_page_config(
    page_title="KPOP", page_icon="❤", layout="centered"
)
st.title("❤ K-Pop")

@st.cache
def get_data(x):
    return pd.read_csv(x)


""" 

### Data about K-Pop idols

Choose home country of the idol:
"""


df = get_data('kpop_idols.csv')


country = st.selectbox('Country', df['Country'].value_counts().iloc[:10].index)


df_selection1 = df[lambda x: x['Country'] == country]
df_selection1

""" 
Choose name of the group you want to know about:
"""
group = st.selectbox('Group', df['Group'].value_counts().index)
df_selection2 = df[lambda x: x['Group'] == group]

df_selection2

beginning_90 = "KPopHits"
ending_90 = "s.csv"
beginning_00 = "KPopHits200"
beginning_01 = "KPopHits20"
ending = ".csv"
names = {}

for i in range(22):
    if i == 0:
        j = 90
        names[str(j)] = beginning_90 + str(j) + ending_90
    elif i > 0 and i <= 10:
        if i == 1:
            j = 0
        names["200" + str(j)] = beginning_00 + str(j) + ending
    else:
        names["20" + str(j)] = beginning_01 + str(j) + ending

    if i != 0:
        j += 1


dict_df = {}


key = list(names.keys())
value = list(names.values())
for i in range(22):
    dict_df[key[i]] = get_data(value[i])


for i in range(22):
    if i == 0:
        period = '1990s'
    else:
        period = key[i]
    danceability = dict_df[key[i]]['danceability'].mean()
    energy = dict_df[key[i]]['energy'].mean()
    loudness = dict_df[key[i]]['loudness'].mean()
    speechiness = dict_df[key[i]]['speechiness'].mean()
    acousticness = dict_df[key[i]]['acousticness'].mean()
    valence = dict_df[key[i]]['valence'].mean()
    tempo = dict_df[key[i]]['tempo'].mean()
    duration = dict_df[key[i]]['duration_ms'].mean()
    if i == 0:
        df2 = pd.DataFrame({'year': [period], 'danceability': [danceability], 'energy': [energy],
                            'loudness': [loudness], 'speechiness': [speechiness],
                            'acousticness': [acousticness], 'valence': [valence], 'tempo': [tempo],
                            'duration_ms': [duration]})
    else:
        row = pd.Series([period, danceability, energy, loudness, speechiness, acousticness,
                         valence, tempo, duration], index=df2.columns)
        df2 = df2.append(row, ignore_index=True)

df2['duration_ms'] = df2['duration_ms']/1000

df3 = pd.melt(df2, id_vars=['year'], value_vars=['danceability', 'energy','loudness', 'speechiness',
                                                 'acousticness', 'valence', 'tempo', 'duration_ms'],
              var_name='category', value_name='value')
df3

df3_first = pd.melt(df2, id_vars=['year'], value_vars=['danceability', "energy", "acousticness", "valence"],
                    var_name='category', value_name='value')

df3_second = pd.melt(df2, id_vars=['year'], value_vars=['speechiness'], var_name='category', value_name='value')

df3_third = pd.melt(df2, id_vars=['year'], value_vars=['tempo', 'duration_ms'], var_name='category', value_name='value')

df3_fourth = pd.melt(df2, id_vars=['year'], value_vars=['loudness'], var_name='category', value_name='value')


g = sns.FacetGrid(df3_first, col='category', hue='category', col_wrap=2)
g = g.map(plt.plot, 'year', 'value')
g = g.map(plt.fill_between, 'year', 'value', alpha=0.2).set_titles("{col_name} category")
g = g.set_titles("{col_name}")


plt.subplots_adjust(top=0.92)
g = g.fig.suptitle('Trend of K-pop')
st.pyplot()


#g = sns.FacetGrid(df3_second, col='category', hue='category', col_wrap=2)
#g = g.map(plt.plot, 'year', 'value')
#g = g.map(plt.fill_between, 'year', 'value', alpha=0.2).set_titles("{col_name} category")
#g = g.set_titles("{col_name}")
#st.pyplot()

g = sns.FacetGrid(df3_third, col='category', hue='category', col_wrap=2)
g = g.map(plt.plot, 'year', 'value')
g = g.map(plt.fill_between, 'year', 'value', alpha=0.2).set_titles("{col_name} category")
g = g.set_titles("{col_name}")
st.pyplot()

#g = sns.FacetGrid(df3_fourth, col='category', hue='category', col_wrap=2)
#g = g.map(plt.plot, 'year', 'value')
#g = g.map(plt.fill_between, 'year', 'value', alpha=0.4).set_titles("{col_name} category")
#g = g.set_titles("{col_name}")
#st.pyplot()

@st.experimental_memo
def get_data1():
    source = df3
    return source


@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["year"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="k-Pop trends")
        .mark_line()
        .encode(
            x="year",
            y="value",
            color="category",
            # strokeDash="category",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(year)",
            y="value",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("year", title="Year"),
                alt.Tooltip("value", title="Value"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


st.write("Give more context to your time series using annotations!")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("Choose a category (⬇💬)", value="‥")
with col2:
    ticker_dx = st.slider(
        "Horizontal offset", min_value=-30, max_value=30, step=1, value=0
    )
with col3:
    ticker_dy = st.slider(
        "Vertical offset", min_value=-30, max_value=30, step=1, value=-10
    )

# Original time series chart. Omitted `get_chart` for clarity
annotation_layer = (
    alt.Chart(df3)
    .mark_text(size=15, text='category', align="center")
    .encode(
        x="year:T",
        y=alt.Y("y:Q"),
    )
    .interactive()
)
source = get_data1()
chart = get_chart(source)

st.altair_chart(chart.interactive(), use_container_width=True)

