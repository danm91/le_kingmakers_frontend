from numpy.lib.twodim_base import tri
import streamlit as st

import datetime
import requests
import plotly.express as px
import plotly.graph_objects as go
from tweets import *
import streamlit.components.v1 as components

#create containers up here: act as subfolders for the page
figure_select = st.beta_container()
most_tweets = st.beta_container()
date_select = st.beta_container()
interactive = st.beta_container()
trial_features = st.beta_container()
lda_features = st.beta_container()
# user_input_features = st.beta_container()

#try to cache one of these to only run once
tweets = Tweets()

#pass this in as a hard-coded list at the end
figures_list = list(tweets.get_data().figure.unique())

#for the plotly graph
figures_group = Tweets().get_data().groupby('figure')


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
              'angelaraynor':'https://pbs.twimg.com/profile_images/1193214910475489281/pZJzUdpD_400x400.jpg',
              'ed_miliband':'https://pbs.twimg.com/profile_images/859337943764410368/Jts3J7JI_400x400.jpg'}


lkm = 'https://i.postimg.cc/HLgtg8vp/Screenshot-2021-06-07-at-12-14-55.png'

with figure_select:
    st.title('Choose political figures')
    chosen_figures = st.multiselect('Select the political figures', figures_list, default='borisjohnson')
    st.markdown(f"{chosen_figures} selected")
    
    #len(figures?) #default lewagon logo
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
    
    # p1_image = p1.image(image_dict.get(chosen_figures[0],lkm))
    # p2_image = p2.image(image_dict.get(chosen_figures[1],lkm))
    # p3_image = p3.image(image_dict.get(chosen_figures[2],lkm))
    # p4_image = p4.image(image_dict.get(chosen_figures[3],lkm))

with most_tweets:
    st.title('some bar charts for the most tweets about, likes and retweets of...')
    st.header('table or chart of percentage likes per negative tweet etc... will work better with numbers from hugging face')
    #st.dataframe(df) - this will plug in the dataframe and let us scroll as necessary
    
with date_select:
    st.header('Choose the dates to filter from')
    
    dates = st.date_input("Default start date is 1st Jan 2021", [datetime.date(2021, 1, 1), 
                                                              datetime.date(2021,1,10)])
    start = str(dates[0])
    finish = str(dates[1])
    
    
    

with interactive:
    st.header('this is an interactive chart from plotly')
    
    concat_list = []
    for figure in chosen_figures:
        df_ = figures_group.get_group(figure)
        df_ = df_[(df_['date']>start) & (df_['date']<finish)]
        df_ = df_.groupby('date').agg({'popularity':'sum'})
        df_['figure'] = figure
        concat_list.append(df_)

    graph_data = pd.concat(concat_list,axis=0)

    #graph:
    fig = px.line(graph_data, x=graph_data.index, y="popularity", color='figure',
                  labels = dict(x = "Date", popularity = "Popularity", figure="Figure"))
    fig.update_layout(title_text='My plotly graph!!!', title_font_size=30,
                      width = 1200, height = 500)
    
    st.write(fig)

    
    
    # fig = go.Figure()
    # fig.update_layout(data=go.Table(header=dict(values=list(graph_data.columns)),
    #                                 cells=dict(values=graph_data.values)))
    # st.write(fig)


with lda_features:
    st.header('LDA Model')
    HtmlFile = open('lda.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, width=1200,height=800, scrolling=True)
#this is html file downloaded and copied directly into the folder, needs to be done again for presentation

with trial_features:
    st.header('Trial with hugging face:')
    predict_side, output_side = st.beta_columns(2)
    # test = st.slider('Questions about the slider', min_value = 5, max_value = 15)
    default_tweet = 'this guy sucks'
    user_text = predict_side.text_area('Enter your twitter message here:', default_tweet)
    
    #hit api
    url='http://127.0.0.1:8000/predict?text='+str(user_text)
    response = requests.get(url,'prediction')
    prediction = response.json()
    if prediction['prediction'] == str(4):
        output_text = 'This conveys positive sentiment'
    else:
        output_text = 'This conveys negative sentiment'
    output_side.text_area('Our model says:', output_text)
