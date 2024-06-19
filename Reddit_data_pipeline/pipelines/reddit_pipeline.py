from etls.reddit_etl import reddit_etl, extract_posts, transform_data, load_data_to_csv
from utils.constants import CLIENT_ID, CLIENT_SECRET, OUTPUT_PATH
import pandas as pd


def reddit_pipeline(filename:str, subreddit:str, time_filter='day', limit=None):
    # Connecting to reddit instance
    instance = reddit_etl(CLIENT_ID, CLIENT_SECRET, user_agent='aws_project')
    # we are doing extraction
    posts = extract_posts(instance, subreddit, time_filter, limit)
    post_df = pd.DataFrame(posts)
    # transformation of the data
    post_df = transform_data(post_df)
    # loading the data to the file
    file_path = f'{OUTPUT_PATH}/{filename}.csv'
    load_data_to_csv(post_df, file_path)
    return file_path


