from dataclasses import field, fields
import encodings
from itertools import count, groupby
from multiprocessing import Condition
from re import U
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math as math
import time 
import streamlit as st
plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = [14,14]
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.cluster import MiniBatchKMeans


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
#col1, col2, col3 = st.columns(3)
#with col1:
 #   st.image("netflix_logo1.jpg", width = 200)
#with col2:
 #   st.image("disney_logo.jpg", width = 200)
#with col3:
 #   st.image("hulu_logo.jpg", width = 200)

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

st.title("Prediction")
ans1 = ""
ans1 = st.text_input("Movie Name")




    

# load the data
df1 = pd.read_csv('netflix_titles.csv')
# convert to datetime
df1["date_added"] = pd.to_datetime(df1['date_added'])
df1['year'] = df1['date_added'].dt.year
df1['month'] = df1['date_added'].dt.month
df1['day'] = df1['date_added'].dt.day
# convert columns "director, listed_in, cast and country" in columns that contain a real list
# the strip function is applied on the elements
# if the value is NaN, the new column contains a empty list []
df1['directors'] = df1['director'].apply(lambda l: [] if pd.isna(l) else [i.strip() for i in l.split(",")])
df1['categories'] = df1['listed_in'].apply(lambda l: [] if pd.isna(l) else [i.strip() for i in l.split(",")])
df1['actors'] = df1['cast'].apply(lambda l: [] if pd.isna(l) else [i.strip() for i in l.split(",")])
df1['countries'] = df1['country'].apply(lambda l: [] if pd.isna(l) else [i.strip() for i in l.split(",")])

df1.head(10)
start_time = time.time()
text_content = df1['description']
vector = TfidfVectorizer(max_df=0.4,         # drop words that occur in more than X percent of documents
                             min_df=1,      # only use words that appear at least X times
                             stop_words='english', # remove stop words
                             lowercase=True, # Convert everything to lower case 
                             use_idf=True,   # Use idf
                             norm=u'l2',     # Normalization
                             smooth_idf=True # Prevents divide-by-zero errors
                            )
tfidf = vector.fit_transform(df1['description'].apply(lambda x: np.str_(x)) )

# Clustering  Kmeans
k = 200
kmeans = MiniBatchKMeans(n_clusters = k)
kmeans.fit(tfidf)
centers = kmeans.cluster_centers_.argsort()[:,::-1]
terms = vector.get_feature_names()

# print the centers of the clusters
# for i in range(0,k):
#     word_list=[]
#     print("cluster%d:"% i)
#     for j in centers[i,:10]:
#         word_list.append(terms[j])
#     print(word_list) 
    
request_transform = vector.transform(df1['description'].apply(lambda x: np.str_(x)))
# new column cluster based on the description
df1['cluster'] = kmeans.predict(request_transform)

df1['cluster'].value_counts().head()



# Find similar : get the top_n movies with description similar to the target description 
def find_similar(tfidf_matrix, index, top_n = 5):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [index for index in related_docs_indices][0:top_n]


G = nx.Graph(label="MOVIE")
start_time = time.time()
for i, rowi in df1.iterrows():
    if (i%1000==0):
        print(" iter {} -- {} seconds --".format(i,time.time() - start_time))
    G.add_node(rowi['title'],key=rowi['show_id'],label="MOVIE",mtype=rowi['type'],rating=rowi['rating'])
#    G.add_node(rowi['cluster'],label="CLUSTER")
#    G.add_edge(rowi['title'], rowi['cluster'], label="DESCRIPTION")
    for element in rowi['actors']:
        G.add_node(element,label="PERSON")
        G.add_edge(rowi['title'], element, label="ACTED_IN")
    for element in rowi['categories']:
        G.add_node(element,label="CAT")
        G.add_edge(rowi['title'], element, label="CAT_IN")
    for element in rowi['directors']:
        G.add_node(element,label="PERSON")
        G.add_edge(rowi['title'], element, label="DIRECTED")
    for element in rowi['countries']:
        G.add_node(element,label="COU")
        G.add_edge(rowi['title'], element, label="COU_IN")
    
    indices = find_similar(tfidf, i, top_n = 5)
    snode="Sim("+rowi['title'][:15].strip()+")"        
    G.add_node(snode,label="SIMILAR")
    G.add_edge(rowi['title'], snode, label="SIMILARITY")
    for element in indices:
        G.add_edge(snode, df1['title'].loc[element], label="SIMILARITY")
print(" finish -- {} seconds --".format(time.time() - start_time))



def get_all_adj_nodes(list_in):
    sub_graph=set()
    for m in list_in:
        sub_graph.add(m)
        for e in G.neighbors(m):        
                sub_graph.add(e)
    return list(sub_graph)
def draw_sub_graph(sub_graph):
    subgraph = G.subgraph(sub_graph)
    colors=[]
    for e in subgraph.nodes():
        if G.nodes[e]['label']=="MOVIE":
            colors.append('blue')
        elif G.nodes[e]['label']=="PERSON":
            colors.append('red')
        elif G.nodes[e]['label']=="CAT":
            colors.append('green')
        elif G.nodes[e]['label']=="COU":
            colors.append('yellow')
        elif G.nodes[e]['label']=="SIMILAR":
            colors.append('orange')    
        elif G.nodes[e]['label']=="CLUSTER":
            colors.append('orange')

    nx.draw(subgraph, with_labels=True, font_weight='bold',node_color=colors)
    plt.show()

list_in=["Ocean's Twelve","Ocean's Thirteen"]
sub_graph = get_all_adj_nodes(list_in)
draw_sub_graph(sub_graph)



def get_recommendation(root):
    commons_dict = {}
    for e in G.neighbors(root):
        for e2 in G.neighbors(e):
            if e2==root:
                continue
            if G.nodes[e2]['label']=="MOVIE":
                commons = commons_dict.get(e2)
                if commons==None:
                    commons_dict.update({e2 : [e]})
                else:
                    commons.append(e)
                    commons_dict.update({e2 : commons})
    movies=[]
    weight=[]
    for key, values in commons_dict.items():
        w=0.0
        for e in values:
            w=w+1/math.log(G.degree(e))
        movies.append(key) 
        weight.append(w)
    
    result = pd.Series(data=np.array(weight),index=movies)
    result.sort_values(inplace=True,ascending=False)        
    return result





result10 = ""

result10= get_recommendation(ans1)
st.write(result10)




result = get_recommendation("Ocean's Twelve")
result2 = get_recommendation("Ocean's Thirteen")
result3 = get_recommendation("The Devil Inside")
result4 = get_recommendation("Stranger Things")
print("*"*40+"\n Recommendation for 'Ocean's Twelve'\n"+"*"*40)
print(result.head())
print("*"*40+"\n Recommendation for 'Ocean's Thirteen'\n"+"*"*40)
print(result2.head())
print("*"*40+"\n Recommendation for 'Belmonte'\n"+"*"*40)
print(result3.head())
print("*"*40+"\n Recommendation for 'Stranger Things'\n"+"*"*40)
print(result4.head())


reco=list(result.index[:4].values)
reco.extend(["Ocean's Twelve"])
sub_graph = get_all_adj_nodes(reco)
draw_sub_graph(sub_graph)

reco=list(result4.index[:4].values)
reco.extend(["Stranger Things"])
sub_graph = get_all_adj_nodes(reco)
draw_sub_graph(sub_graph)
