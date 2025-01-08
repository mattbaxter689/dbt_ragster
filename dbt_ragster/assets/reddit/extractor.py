from dagster import (
    AssetExecutionContext,
    asset,
    MetadataValue,
    MaterializeResult,
)
from dbt_ragster.assets.reddit.reddit_extraction import RedditExtractor

extractor = RedditExtractor(init_site="dbt_ragster")


@asset(description="Extract data from certain subreddits")
def reddit_extraction(context: AssetExecutionContext) -> None:
    context.log.info(f"Scopes: {extractor.get_reddit_scopes()}")
    post, comment = extractor.extract_subreddit_posts(
        sub_reddits="dataengineering"
    )
    context.log.info(f"Posts: {post.dtypes}")
    context.log.info(f"Comments: {comment.dtypes}")

    return MaterializeResult(
        metadata={
            "posts": MetadataValue.md(post.head().to_markdown()),
            "comment": MetadataValue.md(comment.head().to_markdown()),
        }
    )
