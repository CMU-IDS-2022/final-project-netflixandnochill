# Final Project Proposal

**GitHub Repo URL**: https://github.com/CMU-IDS-2022/final-project-netflixandnochill

Team: NetflixAndNoChill

Team Members:
Shivani Gampa: sgampa@andrew.cmu.edu

Hamsini Ravishankar: hravisha@andrew.cmu.edu

“Overall, this year marks a downward trend in subscriber growth for Netflix— it’s the company’s lowest growth year since 2015 and about a 50% decrease from its pandemic-inflated 2020 numbers. Consumers have always had many choices when it comes to their entertainment time — a competition that has only intensified over the last 24 months as entertainment companies all around the world develop their own streaming offering,” the company wrote in its letter to shareholders, admitting that “competition may be affecting [its] marginal growth some.”
 This piece of news piqued our interest. We want to understand the strategy content streaming platforms might have to formulate in order to grow and sustain in a market characterized by monopolistic competition **. 

The central question we are trying to answer is ‘What kind of content streaming platforms need to produce to stay relevant around the world?’
The sub-goals of the project are:

1.Comparative study of the various streaming platforms’ current content and how they are differentiating themselves in the market.

2.Predicting focus areas for these streaming platforms for the upcoming years.

These subgoals will help us work our way up in answering the main question.
We will be using four different datasets, one for each platform.Through this project, we plan to perform a comparative study among four major streaming platforms which are: Netflix, Disney+, Amazon Prime Video, Hulu. In this analysis, we would be depicting the various genres these platforms release content in, the volume of releases happening quarterly, any trends and insights through these that can be banked by these platforms for more revenue generation and more viewership. Through this, we can also answer what the differentiating factor is among these four platforms. As we go ahead to study and visualize the differentiating factors for these platforms, these insights can be helpful for screenplay writers, directors, and producers to help them pitch their scripts/shows/movies to specific niche audiences on their respective platforms.
In this project, we will also be developing a prediction model to predict the genres and type of scripts these streaming platforms should be bringing on board to keep up their differentiating factor while also garnering more revenue income and viewership. 

References: https://techcrunch.com/2022/01/20/netflix-q4-2021-results-subscriber-numbers/

** Monopolistic competition characterizes an industry in which many firms offer products or services that are similar (but not perfect) substitutes


Sketching and Data Analysis

Data Cleaning and Pre-processing:
We have chosen four streaming platforms to do a comparative analysis, which are Netflix, Amazon Prime, Disney+, Hulu. All these 4 datasets have 12 similar columns which are a mix of numeric, ordinal, categorical, text and dates. For the amazon prime dataset the null percentage for production countries is very high, we are working on populating the column using IMDB movies dataset and TV shows dataset by performing joins on the data. We will also create new columns based on the date-added variable. (year and month) and perform binning of rating variable (converting numerical value into categorical data) and perform Feature selection by finding a correlation between variables using Pearson Correlation and remove variables with low variance


Sketches:
- To understand optimal content time on each platform.







