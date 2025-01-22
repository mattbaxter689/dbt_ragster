from sqlalchemy import create_engine
import os
from dataclasses import dataclass
from dotenv import load_dotenv

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


engine = create_engine(url=create_conn_str())
