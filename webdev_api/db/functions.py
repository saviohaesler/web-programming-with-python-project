import logging
import os
import sys

from db.adapters.postgresql_repository import PostgreSQLRepository
from db.adapters.sqlite_repository import SQLiteRepository
from db.repository_interface import RepositoryInterface

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def get_repository() -> RepositoryInterface:
    repo: RepositoryInterface = (
        PostgreSQLRepository()
        if os.getenv("USE_POSTGRES", "false") == "true"
        else SQLiteRepository()
    )

    logging.info("Using repository=%s", repo.__class__.__name__)
    return repo
