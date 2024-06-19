import praw
from praw import Reddit
import sys
import numpy as np
import pandas as pd
import logging
from utils.constants import POST_FIELDS
import os
from utils.constants import CLIENT_ID, CLIENT_SECRET, DATABASE_HOST


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def reddit_etl(client_id, client_secret, user_agent) -> Reddit:
    '''This function connects to the Reddit API and returns the Reddit instance.
    Args:
        client_id: str
        client_secret: str
        user_agent: str
    Returns:
        Reddit instance
    '''
    logging.info(f"Checking the value of config variable: {DATABASE_HOST}")
    logging.info(f"Connecting to Reddit with client_id: {client_id}, client_secret: {client_secret}, user_agent: {user_agent}")
    try:
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        print('Connected to Reddit')
        return reddit
    except Exception as e:
        print('connection to Reddit Error: ', e)
        sys.exit(1) # exit the program if there is an error and 1 is returned 
                    # Here 1 repeats the error code


def extract_posts(reddit_instance: Reddit, subreddit: str, time_filter: str, limit=None):
    '''This function extracts the posts from the subreddit.'''

    logging.info("Starting post extraction.")

    try:
        subreddit = reddit_instance.subreddit(subreddit)
        logging.info(f"Connected to subreddit: {subreddit.display_name}")

        posts = subreddit.top(time_filter=time_filter, limit=limit)
        logging.info(f"Fetched top posts with time filter '{time_filter}' and limit '{limit}'")

        post_lists = []

        for post in posts: # Here all the posts are extracted from the subreddit
            post_dict = vars(post) # vars() function returns the __dict__ attribute of the given object
            post_data = {key: getattr(post, key, None) for key in POST_FIELDS if key in post_dict}  # Extract required fields
            post_lists.append(post_data) # Here we are appending the post to the post_lists
            logging.info(f"Processed post: {post_data.get('title', 'No Title')}")

        logging.info("Post extraction completed successfully.")
        return post_lists

    except Exception as e:
        logging.error(f"Error during post extraction: {e}")
        raise


def transform_data(post_df: pd.DataFrame):
    '''This function transforms the data.'''
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    # Here we are converting the created_utc to datetime format
    post_df['over_18'] = np.where((post_df['over_18'] == True), True, False)
    # Here we are converting the over_18 to boolean format
    post_df['author'] = post_df['author'].astype(str)
    # Here we are converting the author to string format
    edited_mode = post_df['edited'].mode()
    # Here we are finding the mode of the edited column
    post_df['edited'] = np.where(post_df['edited'].isin([True, False]),
                                 post_df['edited'], edited_mode).astype(bool)
    # Here we are converting the edited to boolean format
    post_df['num_comments'] = post_df['num_comments'].astype(int)
    # Here we are converting the num_comments to integer format
    post_df['score'] = post_df['score'].astype(int)
    # Here we are converting the score to integer format
    post_df['title'] = post_df['title'].astype(str)

    return post_df


def load_data_to_csv(data: pd.DataFrame, path: str):
    '''This function saves the dataframe to a CSV file.'''
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save the dataframe to CSV
        data.to_csv(path, index=False)
        logging.info(f"Data successfully saved to {path}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")
        raise
