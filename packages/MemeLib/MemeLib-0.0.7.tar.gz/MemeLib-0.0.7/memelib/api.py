import requests
import random
import json

from memelib.errors import *

class DankMemeClient:
    def __init__(self, use_reddit_for_memes: bool = True, reddit_user_agent:str = "MemeLsib"):
        self.memes = {
            "random":"meme()"
        }
        self.meme_subreddits = [
            "/dankmemes",
            "/memes",
            "/wholesomememes"
        ]
        self.agent = reddit_user_agent
        self.usereddit = use_reddit_for_memes
    def meme(self, subreddit = None):
        if self.usereddit and subreddit:
            r = requests.request("GET", f"https://reddit.com/r/{subreddit}/random.json", headers={"user-agent": self.agent})
            req = r.json()
            if r.status_code != 200:
                if r.status_code == 429:
                    raise RateLimitError("Uh-oh, it looks like you were ratelimited! Try changing your user agent by passing it in the `DankMemeClient` call.")
                    return None
                elif r.status_code == 404:
                    raise SubredditNotFoundError("Reddit's API returned a 404 error. Make sure the subreddit that you passed does not include the `r/` in front of it.")
                    return None
                else:
                    raise RedditApiError(f"Reddit's API returned status code {r.status_code}")
                    return None
            data = {
                "title" : req[0]['data']['children'][0]['data']['title'],
                "author" : req"u/{r[0]['data']['children'][0]['data']['author']}",
                "subreddit" : req[0]['data']['children'][0]['data']['subreddit_name_prefixed'],
                "upvotes" : req[0]['data']['children'][0]['data']['ups'],
                "comments" : req[0]['data']['children'][0]['data']['num_comments'],
                "img_url" : req[0]['data']['children'][0]['data']['url'],
                "post_url" : f"https://reddit.com{req[0]['data']['children'][0]['data']['permalink']}"
            }
            return data
        elif self.usereddit and not subreddit:
            subreddit = random.choice(self.meme_subreddits)
            r = requests.request("GET", f"https://reddit.com/r/{subreddit}/random.json", headers={"user-agent": self.agent}).json()
        elif not self.usereddit:
            return("Still in progress")
            raise SubredditNotFoundError("You didn't specify a subreddit")
