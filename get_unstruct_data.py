import requests

from configs import get_reddit_token

def get_subreddit_data():
    headers = {"Authorization": f"bearer {get_reddit_token()}", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    # resume here
    # https://www.reddit.com/dev/api#fullnames
    import pdb;pdb.set_trace()
    return response

get_subreddit_data()