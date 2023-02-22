import praw
import pandas as pd

reddit = praw.Reddit(client_id='0XgCtUySoei1m0c0C50rPg', 
                     client_secret='mtTAgMC-ZKNoCrMjsI99nyDbQ0W31Q', 
                     user_agent='topic modeling')


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
    submission = reddit.submission(url=('https://www.reddit.com'+ posts['url'][0]))
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        comments.append(comment.body)

    return comments


posts = return_top_post('Bitcoin', 'day', 10)
print(posts)
