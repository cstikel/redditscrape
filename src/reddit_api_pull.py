import praw
import pandas as pd
import yaml
import sys
from datetime import date

today = date.today()


with open('/Users/chasstikeleather/Documents/Projects/redditscrape/config.yaml', 'r') as config:
    params = yaml.safe_load(config)

params['subs']

reddit = praw.Reddit(client_id=params['client_id'], 
                     client_secret=params['client_secret'], 
                     user_agent=params['user_agent'])


def return_top_post(sub_name, time, n):
    ''' Takes a subreddit and returns top n post by time in a dataframe'''

    posts = []
    subreddit = reddit.subreddit(sub_name)
    for post in subreddit.top(time_filter=time, limit=n):
        posts.append([post.title, post.score, post.id, post.subreddit, post.permalink, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

    return posts


def get_comments(post_permalink):
    '''Returns the comments from a reddit post'''

    comments = []
    submission = reddit.submission(url=('https://www.reddit.com'+ post_permalink))
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        comments.append(comment.body)

    return comments


def comment_table(comment_list, post_url):
    '''Takes the list of comments and turns into a df that can be joined to url and post'''
    
    df = pd.DataFrame(comment_list)
    df['post_url'] = post_url
    print(df.columns)
    df.columns = ['comments', 'post_url']

    return df


##### This will be put int he main file
posts = pd.DataFrame()
for sub in params['subs']:
    print("Scraping: "+sub)
    temp_posts = return_top_post(sub, 'day', 20)
    temp_posts = temp_posts[temp_posts['num_comments'] != 0]
    comment_df = pd.DataFrame()
    for post in temp_posts.url:
        print("Scraping Comments from: "+ post)
        comments = get_comments(post)
        comment_df = pd.concat([comment_df,comment_table(comments, post)], ignore_index=True)

    temp_posts = temp_posts.merge(comment_df, how='left', left_on='url', right_on='post_url')
    posts = pd.concat([posts, temp_posts], ignore_index=True )



posts.to_csv(f'/Users/chasstikeleather/Documents/Projects/redditscrape/data/raw/CryptoPulls{today}.csv')
