from dataclasses import field, fields
import encodings
from itertools import count, groupby
from multiprocessing import Condition
from re import U
from turtle import color, title, width
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data



# @st.cache
def load_data():
    """
    Implement a function to load the datasets, add a column for Platform name,
    perform data cleaning for country and release year
    """
    
    df_netflix = pd.read_csv("netflix_titles.csv")
    df_disney = pd.read_csv("disney_plus_titles.csv")
    df_hulu = pd.read_csv("hulu_titles.csv")
    df_netflix['Platform'] = "Netflix"
    df_disney['Platform'] = "Disney"
    df_hulu['Platform'] = "Hulu"
    df = pd.concat([df_netflix,df_disney,df_hulu], ignore_index = True)
    df.reset_index(inplace=True)
    df.drop('show_id', axis=1, inplace=True)
    df.loc[:,'country'] = df.country.str.split(', ')
    df = df.explode('country')
    df.drop_duplicates(['title'],keep = "first", inplace = True)
    df['release_year'] = pd.to_datetime(df['release_year'], format = '%Y')
    df['date_added'] = pd.to_datetime(df['date_added'], format = '%Y-%m-%d')
    df['date_added_month'] = df['date_added'].dt.month_name()
    return df
    pass

def getCountryData(df):
    """
    Implement a function to get counts of data based on show type
    """
    country_df = df[["country","type","index"]]
    country_df = country_df.groupby(['country','type']).count().unstack()
    country_df.columns = ['Movie','TV Show']
    country_df = country_df.reset_index().fillna(0)
    country_df = country_df.drop(0, axis = 0)
    country_df['Movie'] = country_df['Movie'].astype('int')
    country_df['TV Show'] = country_df['TV Show'].astype('int')
    country_df['Total_titles'] = country_df['Movie']+country_df['TV Show']
    country_df = country_df.sort_values(by = 'Total_titles', ascending = False)
  
    return country_df
    pass

def getCountryPlatformData(df):
    """
    Implement a function to get country and total titles data,
    add numeric codes to implement choropleth maps 
    """
    
    df_codes = pd.read_csv("countries_codes_and_coordinates.csv")
    df_codes.drop(['Alpha-2 code','Alpha-3 code','Latitude (average)','Longitude (average)'], axis = 1, inplace = True)
    df_codes['Numeric code'] = df_codes['Numeric code'].str.replace('"','')
    cp_df = df[["country",'index','Platform']]
    cp_df = cp_df.groupby(['country','Platform']).count().unstack()
    cp_df.columns = ['Netflix','Disney','Hulu']
    cp_df = cp_df.reset_index().fillna(0)
    cp_df = cp_df.drop(0, axis = 0)
    
    cp_df['Netflix'] = cp_df['Netflix'].astype('int')
    cp_df['Disney'] = cp_df['Disney'].astype('int')
    cp_df['Hulu'] = cp_df['Hulu'].astype('int')
    cp_df['Total_titles'] = cp_df['Netflix']+cp_df['Disney']+cp_df['Hulu']
    cp_df = cp_df.sort_values(by = 'Total_titles', ascending = False)
    temp_df = cp_df.merge(df_codes.rename({'Country':'country'},axis = 1), on = 'country', how = 'left')
    temp_df = temp_df.fillna("0")
    temp_df['Numeric code'] = pd.to_numeric(temp_df['Numeric code'])
    return temp_df
    pass

def getGenreData(df):
    genre_df = df[["listed_in","index"]]
    genre_df.loc[:,'listed_in'] = genre_df.listed_in.str.split(',')
    genre_df = genre_df.explode('listed_in')
    genre_df['listed_in'] = genre_df['listed_in'].str.strip()
    genre_df['listed_in'] = genre_df['listed_in'].replace(["Action-Adventure","Anime Features","Classic Movies","Comedies","Documentaries","Dramas","Game Shows","Historical","International","Lifestyle","Music","Musical",],["Action & Adventure","Anime","Classics","Comedy","Documentary","Drama","Game Show / Competition","History","International Movies","Lifestyle & Culture","Music & Musicals","Music & Musicals"])
    genre_df['listed_in'] = genre_df['listed_in'].replace(["Horror","Stand Up","Stand-Up Comedy","Sketch Comedy","Talk Show","Thrillers"],["TV Horror","Stand-Up Comedy & Talk Shows","Stand-Up Comedy & Talk Shows","Stand-Up Comedy & Talk Shows", "Stand-Up Comedy & Talk Shows","Thriller"])
    genre_df.drop_duplicates(['index'],keep = "first", inplace = True)
    df['genre'] = genre_df['listed_in'].tolist()
    df.drop('listed_in', axis = 1, inplace = True)
    return genre_df

    pass

def get_slice_membership(combined,platformName):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice. We are
    slicing based on platform.
    
    """
    labels = pd.Series([1] * len(combined), index=df.index)
    if platformName:
        labels &= combined['Platform'].isin([platformName])

        
    return labels

def get_slice_genreType(df, platformName,genreName, typeName):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice. We are
    slicing based on platform and genre.
    
    """
    labels = pd.Series([1] * len(df), index = df.index)
    if genreName:
        labels &= df['genre'].isin([genreName])
    if platformName:
        labels &= df['Platform'].isin([platformName])
    if typeName:
        labels &= df['type'].isin([typeName])

    return labels





st.title("Netflix and No Chill")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("netflix_logo1.jpg", width = 200)
with col2:
    st.image("disney_logo.png", width = 200)
with col3:
    st.image("hulu_logo.jpeg", width = 200)

st.write("VARIETY . ACCESSIBILITY . DOLLARS", width = 500)
st.markdown("The main points of focus for OTT Platforms is to provide a wide variety of content to their viewers which is easily accessible to them at a price that binds the former two.\
    To stay relevant and rule the market, platforms need to understand viewers choice of content")

df = load_data()
c_df = getCountryData(df)
temp_df = getCountryPlatformData(df)
genre_df = getGenreData(df)
 

#map and top 10 genres - ratings
source = alt.topo_feature(data.world_110m.url,'countries')
click = alt.selection_single(empty = "all", fields = ['country'])
world = alt.Chart(source, title = "World Map color-coded with the number of titles produced").properties(width = 800, height = 800).mark_geoshape(
).encode(
    color = alt.Color('Total_titles:Q',scale=alt.Scale(scheme="spectral"), legend=alt.Legend(title = "Count of Titles")),
    opacity = alt.condition(click, alt.value(1), alt.value(0.2)),
    tooltip = [
        alt.Tooltip("country:N", title = "Country"),
        alt.Tooltip("Total_titles:Q", title = "Total Titles")
    ]
).transform_lookup(
    lookup = 'id',
    from_ = alt.LookupData(temp_df,'Numeric code',['Total_titles','country'])
).project(
    "naturalEarth1"
).properties(
    width = 500,
    height = 300
).add_selection(click)


bars_genre = alt.Chart(df).properties(
    width = 300,
    height = 300
).mark_bar().encode(
    y = alt.Y("genre:N", sort = '-x', axis= alt.Axis(title="Genre")),
    x = alt.X("count:Q", axis = alt.Axis(title="Count of Titles")),
    color = alt.Color("count()", legend = None)).transform_filter(click).transform_aggregate(
        count = 'count()',
        groupby = ['genre']
    ).transform_window(
        window = [{'op': 'rank', "as":'rank'}],
        sort = [{'field' : 'count', 'order': 'descending'}]
    ).transform_filter(
        ("datum.rank <= 10")
    ).add_selection(click)


bars_rating = alt.Chart(df).properties(
    width = 300,
    height = 300
). mark_bar().encode(
    y = alt.Y("rating:N", sort = '-x', axis = alt.Axis(title="Ratings")),
    x = alt.X("count()", axis = alt.Axis(title = "Count of Titles")),
    color = alt.Color("count()", legend = None)).transform_filter(click).add_selection(click)


charts = bars_genre | bars_rating
st.altair_chart(world & charts)


#slicing 

platform_selectbox= st.selectbox("Platform",df['Platform'].unique())
membership= get_slice_membership(df,platform_selectbox)

click1 = alt.selection_single(empty = "all", fields = ['type'])
typeOfShow = alt.Chart(df[membership], title = "TV Shows vs Movies").properties(width = 300, height = 300).transform_joinaggregate(
        total = 'count(*)').transform_calculate(
            pct = '1/ datum.total').mark_bar(size = 100).encode(
                alt.X("type", title = "Type"),
                alt.Y('sum(pct):Q', axis = alt.Axis(format='.0%', title="Percentage of Titles"), scale=alt.Scale(domain=[0,1])),
                alt.Color("type")
            ).add_selection(click1)


monthAdded = alt.Chart(df[membership], title = "Titles added across Months").properties(width= 300, height = 300).mark_bar().encode(
    x = alt.X("date_added_month", title="Month", sort = '-y'),
    y = alt.Y("count()", title = "Number of Titles Added"),
    color = alt.Color("type")
).transform_filter(click1).add_selection(click1)
st.altair_chart(typeOfShow | monthAdded)


click_legend = alt.selection_single(fields = ['genre'], bind = 'legend')

total = len(df[membership])
genreOfShow = alt.Chart(df[membership], title = "A slice of Genre").properties(width = 600, height = 500).mark_arc().encode(
    color = alt.Color("genre:N"),
    theta = alt.Theta("mycount:Q"),
    tooltip = ['genre','percentage:O'],
    opacity = alt.condition(click_legend, alt.value(1), alt.value(0.2)),
    order = alt.Order(field="mycount", type="quantitative", sort="descending")
).transform_aggregate(
    groupby = ['genre'],
    mycount = "count()",
).transform_calculate(
    percentage = f"round(datum.mycount / {total} * 1000.0) / 10.0 + '%'"
).add_selection(click_legend)

st.write(genreOfShow)



