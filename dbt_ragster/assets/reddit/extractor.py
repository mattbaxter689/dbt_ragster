from dagster import (
    AssetExecutionContext,
    asset,
    MetadataValue,
    MaterializeResult,
)
from dbt_ragster.assets.reddit.reddit_extraction import RedditExtractor
from dbt_ragster.assets.reddit.text_processor import TextProcessor
from dbt_ragster.assets.reddit.db_conn import engine, dataframe_staged_upsert
import pandas as pd
import datetime as dt

extractor = RedditExtractor(init_site="dbt_ragster")
processor = TextProcessor()


@asset(description="Extract data from certain subreddits")
def reddit_extraction(context: AssetExecutionContext) -> MaterializeResult:
    context.log.info(f"Scopes: {extractor.get_reddit_scopes()}")

    post, comment = extractor.extract_subreddit_posts(
        sub_reddits="dataengineering"
    )
    context.log.info(f"Posts: {post.dtypes}")
    context.log.info(f"Comments: {comment.dtypes}")

    post["created_utc"] = pd.to_datetime(post["created_utc"], unit="s")
    comment["created_utc"] = pd.to_datetime(comment["created_utc"], unit="s")

    dataframe_staged_upsert(
        data=post, dest_table="post_data", unique_columns=["id"], engine=engine
    )
    dataframe_staged_upsert(
        data=comment,
        dest_table="comment_data",
        unique_columns=["comment_id"],
        engine=engine,
    )
    context.log.info("Added data to db")

    return MaterializeResult(
        metadata={
            "posts": MetadataValue.md(post.head().to_markdown()),
            "comment": MetadataValue.md(comment.head().to_markdown()),
        }
    )


@asset(deps=[reddit_extraction], description="Prepare subreddit text data")
def prepare_text(context: AssetExecutionContext) -> MaterializeResult:
    context.log.info("Preparing text data")
    processed_data = processor.process_all(engine=engine)

    processed_data["created_utc"] = dt.datetime.now(tz=dt.timezone.utc)

    with engine.begin() as conn:
        processed_data.to_sql(
            name="processed_data", con=conn, if_exists="replace", index=False
        )

    context.log.info("Added processed text to db")

    return MaterializeResult(
        metadata={
            "processed": MetadataValue.md(processed_data.head().to_markdown())
        }
    )
