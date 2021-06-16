import pandas as pd

class Tweets:
    '''
    DataFrame containing all tweets and popularity per tweet, columns for likes.
    Used to collect create new dataframes to be plotted on streamlit.
    '''
        
    def get_data(self):
        return pd.read_csv('tweets_large_ammended.csv')

    #choose figure
    def by_figure(self, figure_twitter_handle, start = '2021-01-01', finish = '2021-06-01'):
        data = self.get_data()
        by_figure =  data.groupby('figure').get_group(figure_twitter_handle)
        grouped_days = by_figure.groupby('date',as_index=False).agg({'popularity':'sum',
                                                 'likes_count':'sum',
                                                'retweets_count':'sum'})
        return grouped_days[(grouped_days['date']>start) & (grouped_days['date']<finish)]

        
   
    #choose region    
    def get_region(self, regions = []):
        pass