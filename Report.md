# Final Project Report

**Project URL**: TODO
**Video URL**: TODO

Short (~250 words) abstract of the concrete data science problem and how the solutions addresses the problem.

## Introduction
VARIETY . ACCESSIBILITY . DOLLARS

The main points of focus for OTT Platforms is to provide a wide variety of content to their viewers which is easily accessible to them at a price that binds the former two. To stay relevant and rule the market, platforms need to understand viewers' choice of the content they would prefer to watch and relish. The viewership through the internet is rising through OTT Platforms, and now is the time for these platforms to reach the right set of audience based on their changing interests. The main problem that we are trying to solve here is “What kind of content streaming platforms need to produce to stay relevant around the world”.\
 With the current hit of the pandemic we can say that recreation too has moved online. The wide variety in content and accessibility has resulted in a higher retention rate on OTT media applications. This major shift has increased competition between these mega platforms and the disruption of content production pipelines is also another aspect that needs to be addressed. Amidst these changing times, OTT platforms are definitely tackling how they can connect with a wider audience and retain that base of viewership. OTT platforms aim to grow their base aggressively and as a solution are divulging into their own productions to create content with a wider reach. This aspect is our major motivation behind trying to solve this problem. We aim to provide these platforms with some insights like what kind of content is being produced in each country and how well it's working for them and what genre has a wider reach and viewership. We have also developed a movie recommendation system to analyze the network around the list of movies recommended. This analysis will help us get a better understanding of what genres are linked through recommendation and how we can use content popularity in defining a niche for a particular OTT platform using which they can differentiate themselves in the market. 


## Related Work
Predicting content popularity on the web has been researched and examined on different types of content like tweets, images and videos. One of the steps that most influences the outcome of predictive models is to define the predictive attributes, their main features and context. The features in focus on predicting video popularity is mainly the textual content like title and description. (Sá et al., 2021) have proposed two techniques that address this problem. The first approach focuses on feature engineering to select relevant predictive features that are yielded from NLP methods. The second approach leverages representation learning techniques to obtain latent features automatically through word embedding.

Portals often rank and categorize content based on past popularity and user appeal, especially for aggregators, where “wisdom of the crowd” provides collaborative filtering to select submissions favored by as many visitors as possible.To predict the future popularity of content, (Szabo & Huberman, 2010) have transformed variables exhibit strong correlations between early and later time periods.

Popularity prediction of online videos, especially the prediction of top-N popular videos is of great importance to support the development of online video services. From the perspective of commercialization, identifying the top-N popular videos helps the video service providers to maximize their profits. (Tan & Zhang, 2019) present a novel popularity prediction model named multi-factor differential influence based on multivariate linear regression. They first enhanced the ability of early view patterns to identify popularity trends, then performed a large-scale analysis of statistical data of early viewers’ attitude related behavior and the long-term popularity of videos. They have also used tags of videos as indicators of their content and jointly trained a multi-layer perceptron (MLP) network on the popularity data and their related social content.

Movie recommender systems automatically generate the list of recommended movies from large movie datasets based on user profiles and or in response to specific queries supplied by users. (Bhatt, 2009) has proposed a framework of multi-genre movie recommender system based on a neuro-fuzzy decision tree methodology. For generating a list of recommended movies from NFDT in response to user queries, they have proposed a modified inference mechanism based on matching and ordering of fuzzy decision tree paths.


## Methods
Data Collection and Cleaning

We have collected  different datasets for each platform and combined them into one by adding a column - “Platform” for differentiating. Our initial scope was to use 4 different platforms i.e Netflix, Hulu, Disney+ and Amazon Prime. But as we dug deep into the datasets, we could see that in Amazon Prime, the ‘country’ field had 93% null values. To populate these datapoints, we have looked into other datasets like IMDB Movies dataset, TMDb Movies dataset etc which have fields like title, country, ratings, genre, runtime and so on. We have tried to join and merge these datasets in order to reduce the percentage of null values in the Amazon Dataset. After performing these operations as well, the percentage of nulls was still high, approximately 70% which was not good for our analysis pertaining to countries and the most trending genres and rating.\The other fields that needed data preprocessing were ‘listed_in’ and ‘country’. These two fields have multiple values separated by a “,”. This string would not have been very intuitive in performing analysis, hence we decided to take the first entry in the string opposed to the entire one. For a movie/TV show that is associated with multiple genres, as per industry standards, they are listed in order of highest association and relevance to the content of the movie. Hence we chose to take the first genre in the list and a similar approach was applied to the country in which a particular movie/TV show was produced. 

Data Visualization

For the interactive data visualizations we have used multiple altair charts like Choropleth Maps, Bar and Pie Charts. For Choropleth Maps we used the underlying world map from the in-built vega_datasets. In these maps, each country internally has an associated ID code. To map the countries in the graphical map to our dataset, we are also required to have these numeric ISO 3166-1’ codes that the transform_lookup can join to the appropriate geometry and populate the map with data as per need. We have also implemented a slicing tool to analyze data pertaining to each platform and find insights involving their title-addition timelines, the type of content being streamed on the platform (i.e Movie or TV Show), the highest genre they are focusing on. These insights have helped us answer some parts of the main problem as to what is currently working for the platforms and where they can develop a niche for themselves. 

Movie Recommendation System

Initially we wanted to build a model to predict the kind of content that these platforms wanted to produce. That is exactly the narrative we have for our visualization. However we hit a number of road blocks. First, there were very few variables that were relevant to this question. The dependent variables:country, rating. The independent variable in this case was ‘listed_in’ (genre). Second, the cardinality of the ‘country’ variable was huge yet we had to use one-hot-encoding to deal with the categorical variable which really increased the dimension of the dataset. Third, which was  the worse for our question was the fact that the important listed categorical variables above had values in their validation set which were not in their test set.The simplest way to deal with this problem was to drop the column entirely. Having seen these many challenges with trying a prediction model for this particular datasets, we decided to change it to elicit more insight.
We decided to build a custom recommendation system for each of our platforms. The ‘description’ attribute was dealt with in 2 ways.\ 
1.Movies are clustered using KMeans clustering with TF-IDF weights.(So two movies that belong in a group of description will share a node.)
2.calculate the TF-IDF matrix and for each film and then take the top 5 of similar descriptions.In this case Adamic Adar measure used to compute closeness between the nodes.


## Results
![image](https://user-images.githubusercontent.com/43342469/165889417-081a708a-c957-4d69-8285-a762b68252d6.png)
This is how the visualizations flow:

First, we try to get an overall picture of the trends prevelant in globally. In the map below you can see that the countries are color coded with number of titles produced. We can see that United States has the maximum number of titles being prodcued followed by India, United Kingdomw, Canada and Australia. Through this visualization we can also gauge the top 10 trending genres and the ratings that they are more focused at. Drama, Comedy, Action and Adventure seem to be the most popular, bringing in high viewrship rates and they also contain content that is for mature audience and may not be suitable for kids below the age of 17
![image](https://user-images.githubusercontent.com/43342469/165889496-e62dd15a-4076-458b-8f12-005ea19d1164.png)

These three visualizations are interconnected, as in, we can select a particular country and the trending genres and rating will populate accordingly. This can help us gain some insight as to what is working in a particular country. This can take things a step further in figuring out the scope of expansion in terms of content being produced, it can also give us a broad idea and pave the way towards identifying a niche for the platforms

![image](https://user-images.githubusercontent.com/43342469/165889887-43245f7e-cfab-423a-96d8-0fd2c56354d3.png)  
![image](https://user-images.githubusercontent.com/43342469/165890721-3ec53475-b6e9-4e18-9005-06f6997b8b41.png)


Now, we move onto Platform-wise analysis to see what are the type of titles being published on these platforms, like Movies or TV shows. We have created another interconnected bar graph to shpw the title addition trends in each platorm. We selct netflix for the first one
![image](https://user-images.githubusercontent.com/43342469/165891196-b94a83f5-211b-4e77-aca0-f37867aa4512.png)
For netflix we can see that, they have a lot of movies compared to TV Shows. We can also see that Netflix focuses more on the Holiday season to relase titles on its platforms, pertaining to a high number of additions in the months fo July, December, Sepetember which correlates to Summer vaction and Christmas-Thanksgiving seaons respectively.
![image](https://user-images.githubusercontent.com/43342469/165891577-603d56d2-1a0b-4070-b211-55e4ce3011ad.png)
Using, the interactive legend, we can see that Drama has the highest percentage of shows followed by comedy, action and adventure. 
Similar trends can be seen on Hulu as well. Hulu too releases most number of titles on its platform during th holiday season. The trneding genres are also in the same order as Netflix. The only difference we can see her is that, Hulu has a lot more number of TV shows compared to Netflix.
![image](https://user-images.githubusercontent.com/43342469/165891998-b8a056a9-d4e8-4558-94e8-87f14c149e0e.png)
![image](https://user-images.githubusercontent.com/43342469/165892049-2d627b8f-de1f-4817-8f51-2047cf8a28e6.png)

For Disney, the trends seem to be a bit different with the top genres. Disnesy seems to be hitting the spot by aiming November as the month for their major number of releases. Their top trending genres are Action and Animantion, righfully so as we have all grown up watching these Disney productions.
![image](https://user-images.githubusercontent.com/43342469/165892479-9cfec7a5-b30b-4eaa-87a8-759b5f84f9e7.png)
![image](https://user-images.githubusercontent.com/43342469/165892514-f7f4f9b7-a2c7-4216-b0ee-4bcf7a03315c.png)






## Discussion

## Future Work
We can extend this project in the following ways:

1. Build a recommendation system that combines all the above datasets. This will enable us to further discover how similar platforms are. It will be interesting because in the real world people have the choice to pick one or more platforms based on the content they have been recommended/watched. The user might be enticed by a recommendation engine that suggests content based on all the platforms they subscribe to. \
2. Another way to advance the project is to incorporate graphs generated from the recommendation engine. The recommendation engine was built for movies, but it can also be extended to TV shows.

