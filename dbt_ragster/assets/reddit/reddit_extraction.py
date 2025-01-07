import praw

class RedditExtractor():
    def __init__(self, init_site: str) -> None:
        self._reddit = praw.Reddit(
            init_site,
            user_agent="Comment extraction by u/bananasman178"
        )      

    def get_reddit(self) -> set[str]:
        return self._reddit.auth.scopes()
