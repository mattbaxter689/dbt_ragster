from dagster import asset, AssetExecutionContext
import os

@asset
def hello(context: AssetExecutionContext) -> None:
    context.log.info("Hello Dagster!!!")
    context.log.info(f"CWD: {os.getcwd()}")