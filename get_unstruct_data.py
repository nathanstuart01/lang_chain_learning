import requests
from urllib3.exceptions import HTTPError
from praw import Reddit

from configs import reddit_token, reddit

def get_related_subreddits(query: str, limit: int = 1):
    headers = {"Authorization": f"bearer {reddit_token}", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get(f"https://oauth.reddit.com/subreddits/search?q={query}", headers=headers)
    if response.status_code == 200:
        return [subreddit['data']['url'] for subreddit in response.json()['data']['children']][:limit]
    else:
        raise HTTPError(f"Error fetching related subreddits. Error code: {response.status_code}")

def get_subreddit_traffic_stats(subreddit: str):
    # work on this to get subredit traffic stats:
    # to prove out the insights gleaned
    # https://www.reddit.com/dev/api/oauth#GET_r_{subreddit}_about_traffic
    pass

def get_subreddit_comments(reddit: Reddit, subreddit: str, type: str = "hot"):
    # resume here with getting comments from the threads, start with hottest
    # https://www.reddit.com/r/explainlikeimfive/comments/1u0q4s/eli5_difference_between_best_hot_and_top_on_reddit/
    # use PRAW: https://praw.readthedocs.io/en/stable/
    if type == "hot":
        for submission in reddit.subreddit(subreddit).hot(limit=25):
            import pdb;pdb.set_trace()
            print(submission.title)

get_subreddit_comments(reddit, "Seahawks")