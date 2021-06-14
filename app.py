
from numpy.lib.twodim_base import tri
import streamlit as st

import datetime

import requests

from tweets import *

'''
attempt to run on streamlit
'''
#create containers up here: going to fill them in afterwards - breakdown of the 

figure_select = st.beta_container()
date_select = st.beta_container()
trial_features = st.beta_container()

#functions:
@st.cache
def get_popularity(list_of_figures):
    empty_df = sorted(Tweets().get_data()['date'].unique())
    empty_df = pd.DataFrame(empty_df,columns=['date'])
    for figure in list_of_figures:
        fig_tweets = Tweets().by_figure(figure)
        fig_tweets = fig_tweets.rename({'popularity':figure},axis=1)
        fig_tweets = fig_tweets[['date',figure]]
        empty_df = empty_df.merge(fig_tweets, on='date')
    return empty_df


tweets = Tweets()

#pass this in as a hard-coded list at the end
political_figures_list = list(tweets.get_data().figure.unique())


with figure_select:
    st.title('Choose political figures')
    figures = st.multiselect('Select the political figures', political_figures_list)
    

with date_select:
    st.header('Choose the dates to filter from')
    
    d3 = st.date_input("Default start date is 1st Jan 2021", [datetime.date(2021, 1, 1), 
                                                              datetime.date(2021,1,10)])
    start = str(d3[0])
    finish = str(d3[1])

    graph_data = get_popularity(figures)
    graph_data = graph_data[(graph_data['date']>start) & (graph_data['date']<finish)]
    
    #graph:
    st.line_chart(data=graph_data.set_index('date'))


with trial_features:
    sel_col,disp_col = st.beta_columns(2)
    test = sel_col.slider('Questions about the slider', min_value = 5, max_value = 15)
    st.markdown(f"you've selected {test}")
    default_tweet = 'this guy sucks'
    st.header('Trial with hugging face:')
    sel_col.text_input('Enter your twitter message here:', default_tweet)
    #run through hugging face model and return - will need an api call#
    




# d5 = st.date_input("date range without default", [datetime.date(2021, 6, 1), datetime.date(2019, 7, 8)])
# st.write(d5)

# d3 = st.date_input("range, no dates", [])
# st.write(d3)



# enter here the address of your flask api
url = 'https://taxifare.lewagon.ai/predict'

params = dict(
    start=start,
    finish=finish,
    # figure=figure,
    )

response = requests.get(url, params=params)

prediction = response.json()

pred = prediction['prediction']

pred
