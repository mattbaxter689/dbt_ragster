from dagster import AssetExecutionContext, asset
from dbt_ragster.assets.reddit.reddit_extraction import RedditExtractor

extractor = RedditExtractor(init_site="dbt_ragster")


@asset(description="Extract data from certain subreddits")
def reddit_extraction(context: AssetExecutionContext) -> None:
    context.log.info("Hello Dagster!!!")
    context.log.info(f"Scopes: {extractor.get_reddit()}")
