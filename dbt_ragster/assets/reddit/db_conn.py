from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os
from dataclasses import dataclass
from sqlalchemy import text
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()


@dataclass
class DBConnection:
    db: str
    user: str
    password: str
    host: str
    port: int


def create_conn_str() -> str:

    def get_warehouse_creds() -> DBConnection:
        return DBConnection(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            db=os.getenv("POSTGRES_DB"),
            host="dbt_ragster_db",
            port=os.getenv("POSTGRES_PORT"),
        )

    db_conn = get_warehouse_creds()

    conn_url = (
        f"postgresql+psycopg2://{db_conn.user}:{db_conn.password}@"
        f"{db_conn.host}:{db_conn.port}/{db_conn.db}"
    )

    return conn_url


def staging_table_name_generator():
    np.random.seed()
    A, Z = np.array(["A", "Z"]).view("int32")
    staging_table = np.random.randint(
        low=A, high=Z, size=20, dtype="int32"
    ).view(f"U{20}")[0]

    return "STAGING_" + staging_table


def dataframe_staged_upsert(
    data: pd.DataFrame,
    dest_table: str,
    unique_columns: list[str],
    engine: Engine,
    retries: int = 3,
) -> None:
    if not isinstance(unique_columns, list):
        raise ValueError("Unique columns must be of type list")

    staging_table = staging_table_name_generator()

    upload_success = False
    columns = data.columns.to_list()

    drop_table_statement = f'DROP TABLE "{staging_table}";'
    upsert_query = " ".join(
        f"""
        INSERT INTO "{dest_table}" ({', '.join([f'"{x}"' for x in columns])})
        SELECT {', '.join([f'"{x}"' for x in columns])} FROM "{staging_table}"
        ON CONFLICT ({', '.join([f'"{x}"' for x in unique_columns])}) DO UPDATE
        SET {', '.join([f'"{x}" = EXCLUDED."{x}"' for x in columns])};
        """.replace(
            "\n", ""
        )
        .replace("\r", "")
        .split()
    )

    retries_left = retries if retries > 0 else 1
    while retries_left > 0:
        data.to_sql(
            staging_table,
            engine,
            if_exists="replace",
            index=False,
            index_label=unique_columns,
        )
        with engine.begin() as conn:
            try:
                conn.execute(text(upsert_query))
                retries_left = 0
                upload_success = True

            except Exception as e:
                print(e)
                retries_left -= 1
                conn._transaction.rollback()
                try:
                    conn.execute(text(drop_table_statement))
                except Exception as e:
                    print(f"Failed to drop staging table: {e}")
        if upload_success:
            try:
                with engine.begin() as conn:
                    conn.execute(text(drop_table_statement))
            except Exception as e:
                print(f"Failed to drop staging table: {e}")

    if upload_success:
        return


engine = create_engine(url=create_conn_str())
