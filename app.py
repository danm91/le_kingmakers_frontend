from numpy.lib.twodim_base import tri
import streamlit as st

import datetime
import requests
import plotly.express as px
import plotly.graph_objects as go
from tweets import *
import streamlit.components.v1 as components
import numpy as np

import json  #  SEB ADDED
from geojson_rewind import rewind  #  SEB ADDED
import os 


st.set_page_config(page_title='Le KingMakers', page_icon=None, layout='wide', initial_sidebar_state='auto')
lkm = 'https://i.postimg.cc/HLgtg8vp/Screenshot-2021-06-07-at-12-14-55.png'

left,mid,right = st.beta_columns(3)
# left.markdown(st.image(lkm, width = 60))
mid.markdown("<h1 style='text-align: center;color: rgb(255, 0, 0);'>Le KingMakers</h1>", unsafe_allow_html=True) 

#create containers up here: act as subfolders for the page
figure_select = st.beta_container()
tweet_table = st.beta_container()
date_select = st.beta_container()
interactive = st.beta_container()
tweet_fetcher = st.beta_container()
uk_map = st.beta_container()
NB_sentiment = st.beta_container()
trial_features = st.beta_container()
scraping = st.beta_container()
lda_features = st.beta_container()
# user_input_features = st.beta_container()

make_choice = st.sidebar.selectbox('Welcome!', ['Home Page',
                                                'Twitter Sentiment Evaluation', 'Experimental'])

tweets = Tweets()
df = Tweets().get_data()
df = df.iloc[:,1:].rename(columns={'scores':'popularity'})
df.date = pd.to_datetime(df.date)

#pass this in as a hard-coded list at the end
figures_list = ['borisjohnson', 'davidlammy', 'keir_starmer',
       'matthancock', 'grantshapps', 'jonashworth', 'lisanandy',
       'pritipatel', 'rishisunak', 'angelarayner', 'dominicraab',
       'ed_miliband', 'jeremycorbyn', 'michaelgove', 'emilythornberry']

#for the plotly graph
figures_group = df.groupby('figure')


#Figure dict of urls for photos
image_dict = {'borisjohnson':'https://pbs.twimg.com/profile_images/1331215386633756675/NodbPVQv_400x400.jpg',
              'matthancock':'https://pbs.twimg.com/profile_images/1311368965160136704/ypBTtBpn_400x400.jpg',
              'jeremycorbyn':'https://pbs.twimg.com/profile_images/1351939685900288007/lcoCyR7S_400x400.jpg',
              'keir_starmer':'https://pbs.twimg.com/profile_images/1323314457892790276/EfBgm41w_400x400.jpg',
              'davidlammy':'https://pbs.twimg.com/profile_images/1334893581874716683/nI8J96l2_400x400.jpg',
              'pritipatel':'https://pbs.twimg.com/profile_images/1260148688334270465/ouBRXPoz_400x400.jpg',
              'grantshapps':'https://pbs.twimg.com/profile_images/1395400250941136898/O8hM9jG__400x400.jpg',
              'rishisunak':'https://pbs.twimg.com/profile_images/1372190965599985664/PQ3J2v6Y_400x400.jpg',
              'dominicraab':'https://pbs.twimg.com/profile_images/1380436741929246720/MhnVuFB7_400x400.jpg',
              'michaelgove':'https://pbs.twimg.com/profile_images/1143081469969096704/5ovqIK49_400x400.jpg',
              'emilythornberry':'https://pbs.twimg.com/profile_images/1325943690456608774/JQqkdbFA_400x400.jpg',
              'jonashworth':'https://pbs.twimg.com/profile_images/1286568704751415297/eOv71dI3_400x400.jpg',
              'lisanandy':'https://pbs.twimg.com/profile_images/1242221937939689474/MqMEU5Ja_400x400.jpg',
              'angelarayner':'https://pbs.twimg.com/profile_images/1193214910475489281/pZJzUdpD_400x400.jpg',
              'ed_miliband':'https://pbs.twimg.com/profile_images/859337943764410368/Jts3J7JI_400x400.jpg'}


if make_choice == 'Home Page':


#SELECT FIGURES ------------------------------------------------------------------------------------------------ 
    with figure_select:
        st.title('Who should we judge sentiment for?')
        chosen_figures = st.multiselect('Select political figures:', figures_list, default=['borisjohnson', 'keir_starmer'])
        
        num_figures = len(chosen_figures)
        
        def func(length,num_figures=num_figures):
            num_index=[]
            for num in range(num_figures):
                num_index.append(f"p{num}")
            return num_index #list of variables, p0,p1 etc...
        
        num_index = func(num_figures)
        
        locals()[','.join(func(num_figures))] = st.beta_columns(len(num_index)) 
        #turn list to string then evaluate to variables to assign to the beta_columns
        for i in range(num_figures):
            locals()[','.join(func(num_figures))][i].image(image_dict.get(chosen_figures[i],lkm))

#SELECT FIGURES ------------------------------------------------------------------------------------------------    

#Random_Tweet------------------------------------------------------------------------------------------------ 

# this can be split into getting a positive and negative tweet

    with tweet_fetcher:
        st.title('Tweet Fetcher')
        pol = st.selectbox('Fetch me a tweet about: ', options = figures_list)
        day = st.slider('Date selection', datetime.datetime.strptime('2021-01-01', '%Y-%m-%d'),
                datetime.datetime.strptime('2021-06-10', '%Y-%m-%d'), 
                datetime.datetime.strptime('2021-06-01','%Y-%m-%d'))
        if st.button('Get me a tweet'):
            day_dt = datetime.datetime.date(day)
            st.table(df.loc[(df['figure']==pol) &(
                df['date'] == str(day_dt)),['tweet','likes_count', 'retweets_count','popularity']].sample(1))
                     
                    
#Random_Tweet------------------------------------------------------------------------------------------------


#DISPLAY TWEETS ------------------------------------------------------------------------------------------------ 
    with tweet_table:
        # st.title('some bar charts for the most tweets about, likes and retweets of...')
        def func(x):
            if x in chosen_figures:
                return 1
            else:
                return 0
        
        df['fig'] = df['figure'].map(func)
        df2 = df[df['fig'] == 1]
        
        st.title('What have people been saying?')
        st.table(df2[['tweet','popularity']].rename(columns = {'tweet':'Tweet',
                                                            'popularity':'Popularity'}).sample(5))
#DISPLAY TWEETS ------------------------------------------------------------------------------------------------ 

 

#DATE SELECT ------------------------------------------------------------------------------------------------ 
    with date_select:
        st.title('Select dates to compare popularity')
        
        dates = st.date_input("Default start date is 1st Jan 2021", [datetime.date(2021, 1, 1), 
                                                                datetime.date(2021,6,10)])
        start = str(dates[0])
        finish = str(dates[1])
#DATE SELECT ------------------------------------------------------------------------------------------------ 

    
    
#PLOTLY#------------------------------------------------------------------------------------------------      
    with interactive:
        st.header(' ')
        
        likes_w = 0.2
        retweets_w = 0.6
        
        concat_list = []
        for figure in chosen_figures:
            df_ = figures_group.get_group(figure)
            df_ = df_[(df_['date']>start) & (df_['date']<finish)]
            df_['popularity'] = df_['popularity'] * (likes_w*df_['likes_count'] + retweets_w*df_['retweets_count'])
            df_ = df_.groupby('date').agg({'popularity':'mean'})
            df_['figure'] = figure
            concat_list.append(df_)

        graph_data = pd.concat(concat_list,axis=0)
            
        #graph:
        fig = px.line(graph_data, x=graph_data.index, y="popularity", color='figure',
                    labels = dict(x = "Date", popularity = "Popularity", figure="Figure"))
        fig.update_layout(title_text='Popularity Over Time', title_font_size=30,
                        width = 1200, height = 500)
        
        st.write(fig)
#PLOTLY#------------------------------------------------------------------------------------------------ 


#UK MAP ------------------------------------------------------------------------------------------------ 

# importing map
    with uk_map:
        st.title('UK Sentiment Map')
        # map_side, select_side = st.beta_columns(2)
        # st.header('Map View of <INSERT FIGURE>')
        
        map_politician = st.selectbox("MP selection", options = chosen_figures)
        
        geojson_path = 'geojson_full_extent_super_gen.geojson'
        with open(geojson_path) as json_file:
            uk_regions_json = json.load(json_file)
            
        # locations dictionary
        location_dict = {}
        for feature in uk_regions_json['features']:
            location_dict[feature['properties']['nuts118nm']] = [feature['properties']['lat'],feature['properties']['long']]
        # regions dictionary
        region_id = {}
        for feature in uk_regions_json['features']:
            region_id[feature['properties']['nuts118nm']] = feature['properties']['nuts118cd']
        

        geo_locations = list(region_id.keys())
        politician_df = df[df.figure==map_politician]
        politician_df = politician_df[['date','geo','retweets_count','likes_count','popularity']]
        temp_group = politician_df.groupby('geo')
        geo_concat=[]
        
        for geo in geo_locations:
            df_ = temp_group.get_group(geo)
            df_ = df_[(df_['date']>start) & (df_['date']<finish)]
            df_ = df_.groupby('geo', as_index=False).agg({'popularity':'mean'})
            geo_concat.append(df_)

        geo_data = pd.concat(geo_concat,axis=0)
        geo_data.geo = geo_data.geo.map(region_id) 
        geo_data.rename(columns = {'popularity':'Popularity'},inplace=True)  
            
    # -------------------END OF DF IMPORT-----------------------------------------
    # plot results
        counties_corrected = rewind(uk_regions_json,rfc7946=False)
        fig = px.choropleth(geo_data, geojson=counties_corrected, locations='geo', featureidkey="properties.nuts118cd", color='Popularity',
                                    color_continuous_scale="RdYlGn", color_continuous_midpoint=-0.35,
                                    labels={'label name':'label name'}, scope="europe") 
                                    # title='MAP TITLE'
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(width=800, height=800)
        
        map_side, blank_mid, pol_side = st.beta_columns(3)
        map_side.plotly_chart(fig)
        pol_side.image(image_dict.get(map_politician))

#UK MAP ------------------------------------------------------------------------------------------------ 


if make_choice == 'Experimental':
    with lda_features:
        st.title('Latent Dirichlet Allocation')
        HtmlFile = open('lda.html', 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, width=1200,height=800, scrolling=True)
#this is html file downloaded and copied directly into the folder, needs to be done again for presentation

if make_choice == 'Twitter Sentiment Evaluation':
    with NB_sentiment:
        st.title('Machine Learning Model Prediction:')
        predict_side, output_side = st.beta_columns(2)
        # test = st.slider('Questions about the slider', min_value = 5, max_value = 15)
        default_tweet = 'I love Le Wagon'
        user_text = predict_side.text_area('Enter your twitter message here:', default_tweet)
        
        gcp_predict= 'https://api-6pnntkepya-ew.a.run.app/predict?text='    
        
        url = gcp_predict+str(user_text)
        response = requests.get(url,'prediction')
        if response.json() > 0:
            prediction = 'This conveys positive sentiment'
        else:
            prediction = 'This conveys negative sentiment'
        
        output_side.text_area('Our model says:', prediction)

        
        st.title('From the friendly folks at Hugging Face and Cardiff University:')
        predict_side2, output_side2 = st.beta_columns(2)
        
        #hugging face#
        user_input = predict_side2.text_area('The same tweet:', 'Enter message here')
        url=gcp_predict+str(user_input)
        response = requests.get(url,'prediction')
        prediction = response.json()
        output_side2.text_area('CardiffNLP says:', prediction)
        
        
        
        # if user_input != user_text:
        #     url = gcp_predict+str(user_input)
        #     response = requests.get(url,'prediction')
        #     output_side2.text_area('cardiffnlp says:', str(response.json()))
        # else:
        #     hf_response = output_side2.text_area('cardiffnlp says:', str(prediction))
        

    with scraping:
        st.title('Twitter scraping tool')
        gcp_scrape= 'https://api-6pnntkepya-ew.a.run.app/scrapeandpredict'
    
        user_tweet = st.text_area('Enter your tweet')
        if st.button('Scrape tweets'):
            # st.markdown('okay')
            response = requests.get(gcp_scrape,params={'search': user_tweet})
            df_scrape = pd.read_json(response.json())
            st.table(df_scrape[['tweet','scores']].sample(10))
    
# have a model for naive bayes
# separate section for the hugging face