import praw
import pandas as pd
from typing import Iterator, Any


class RedditExtractor:
    def __init__(self, init_site: str) -> None:
        self._reddit = praw.Reddit(
            init_site, user_agent="Comment extraction by u/bananasman178"
        )

    def get_reddit_scopes(self) -> set[str]:
        """Display scopes for current refresh token

        Returns:
            set[str]: a set of the current scopes
        """
        return self._reddit.auth.scopes()

    def extract_subreddit_posts(
        self, sub_reddits: str | list[str]
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Extract data from specified subreddits

        Args:
            sub_reddits (str | list[str]): The subreddit(s) to get data

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: the posts and comment data
        """

        # convert single subreddit instance so we can iterate regardless
        if isinstance(sub_reddits, str):
            sub_reddits = [sub_reddits]

        for reddit in sub_reddits:
            sub_data = self._reddit.subreddit(reddit)
            posts = []
            comments = []
            for post in sub_data.hot(limit=30):
                post.comments.replace_more(limit=100)
                extracted_comments = self.extract_post_comments(
                    comments=post.comments
                )
                comments.extend(extracted_comments)

                post_data = {
                    "title": post.title,
                    "selftext": post.selftext,
                    "score": post.score,
                    "post_url": post.url,
                    "id": post.id,
                    "distinguished": post.distinguished,
                    "locked": post.locked,
                    "is_original_content": post.is_original_content,
                    "spoiler": post.spoiler,
                    "author": str(post.author),
                    "created_utc": post.created_utc,
                    "num_comments": post.num_comments,
                    "upvote_ratio": post.upvote_ratio,
                    "subreddit": str(post.subreddit),
                }
                posts.append(post_data)

        return pd.DataFrame(posts), pd.DataFrame(comments)

    def extract_post_comments(
        self, comments: Iterator[Any]
    ) -> list[dict[str, Any]]:
        all_comments = []
        for comment in comments:
            comment_data = {
                "body": comment.body,
                "author": str(comment.author),
                "score": comment.score,
                "distinguished": comment.distinguished,
                "edited": bool(comment.edited),
                "created_utc": comment.created_utc,
                "is_top_level": comment.is_root,
                "depth": comment.depth,
                "is_submitter": comment.is_submitter,
                "post_id": str(comment.link_id).replace("t3_", ""),
                "comment_id": comment.id,
            }
            all_comments.append(comment_data)
        return all_comments
