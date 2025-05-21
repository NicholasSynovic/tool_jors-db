"""
Handle database IO operations.

Copyright 2025 (C) Software and Systems Laboratory
"""

from pathlib import Path
from pandas import DataFrame
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    Engine,
    ForeignKey,
    DateTime,
    JSON,
)


class DB:
    """
    A class for interacting with a SQLite database.

    This class provides methods for initializing the database, creating tables,
    and inserting data from Pandas DataFrames.

    """

    def __init__(self, fp: Path) -> None:
        """
        Initialize SQLite3 database.

        This constructor creates a SQLAlchemy engine for interacting with a
        SQLite database. It uses the provided file path (fp) to create a
        database file. The metadata object is initialized to manage the database
        schema.

        Args:
            fp: A Path object representing the file path to the SQLite database.

        """
        self.engine: Engine = create_engine(url=f"sqlite:///{fp}")
        self.metadata: MetaData = MetaData()
        self._create_tables()

    def _create_tables(self) -> None:
        """
        Create database tables for storing JORS paper metadata.

        This method defines and creates three tables: 'front_matter',
        'metadata', and 'software'. The 'front_matter' table stores the raw HTML
        content of the papers. The 'metadata' table stores structured metadata
        extracted from the HTML. The 'software' table stores additional
        information about the software projects.

        It uses the SQLAlchemy engine and metadata objects to define the table
        schemas and then executes the `create_all()` method to create the tables
        in the database.

        """
        _: Table = Table(
            "front_matter",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("url", String, nullable=False),
            Column("page", Integer, nullable=False),
            Column("status_code", Integer, nullable=False),
            Column("html", String, nullable=False),
        )

        _: Table = Table(
            "paper_metadata",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column(
                "front_matter_id",
                Integer,
                ForeignKey("front_matter.id"),
                nullable=False,
            ),
            Column("doi", String, nullable=False),
            Column("title", String, nullable=False),
            Column("publication_date", DateTime, nullable=True),
            Column("authors", JSON, nullable=True),
        )

        self.metadata.create_all(bind=self.engine, checkfirst=True)

    def df2table(self, df: DataFrame, table: str) -> None:
        """
        Insert Pandas DataFrame into the database table.

        This method takes a Pandas DataFrame and a table name as input and inserts the
        data from the DataFrame into the specified table in the database. It uses the
        SQLAlchemy engine to interact with the database.

        Args:
            df: A Pandas DataFrame containing the data to be inserted.
            table: The name of the table to insert the data into.

        """
        df.to_sql(
            name=table,
            con=self.engine,
            if_exists="append",
            index=True,
            index_label="id",
        )
