from dagster import (
    AssetExecutionContext,
    asset,
    MetadataValue,
    MaterializeResult,
)
from dbt_ragster.assets.reddit.reddit_extraction import RedditExtractor
from dbt_ragster.assets.reddit.db_conn import engine
import pandas as pd

extractor = RedditExtractor(init_site="dbt_ragster")


@asset(description="Extract data from certain subreddits")
def reddit_extraction(context: AssetExecutionContext) -> None:
    context.log.info(f"Scopes: {extractor.get_reddit_scopes()}")

    post, comment = extractor.extract_subreddit_posts(
        sub_reddits="dataengineering"
    )
    context.log.info(f"Posts: {post.dtypes}")
    context.log.info(f"Comments: {comment.dtypes}")

    post["created_utc"] = pd.to_datetime(post["created_utc"], unit="s")
    comment["created_utc"] = pd.to_datetime(comment["created_utc"], unit="s")

    with engine.begin() as conn:
        post.to_sql(
            name="post_data", con=conn, if_exists="append", index=False
        )

        comment.to_sql(
            name="comment_data", con=conn, if_exists="append", index=False
        )
    context.log.info("Added data to db")

    return MaterializeResult(
        metadata={
            "posts": MetadataValue.md(post.head().to_markdown()),
            "comment": MetadataValue.md(comment.head().to_markdown()),
        }
    )
