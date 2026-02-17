"""
Database connection and session management for Databricks Postgres Lakebase
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from typing import Generator
import requests
from urllib.parse import quote_plus
import logging
import os

from utility.ORM import Base

logger = logging.getLogger(__name__)

# OAuth credentials for Lakebase
CLIENT_ID = os.getenv("LAKEBASE_USERNAME")
CLIENT_SECRET = os.getenv("LAKEBASE_PASSWORD")
LAKEBASE_HOST = os.getenv("LAKEBASE_HOST")
LAKEBASE_PORT = os.getenv("LAKEBASE_PORT")
DATABRICKS_HOST = os.getenv("DATABRICKS_SERVER_HOSTNAME")
SCHEMA_NAME = os.getenv("LAKEBASE_SCHEMA", "default")


def get_oauth_token() -> str:
    """
    Get OAuth access token for Lakebase
    
    Returns:
        Access token string
    """
    token_url = f"https://{DATABRICKS_HOST}/oidc/v1/token"
    
    try:
        response = requests.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "scope": "all-apis"
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        logger.error(f"Failed to get OAuth token: {str(e)}")
        raise


# Get fresh OAuth token
access_token = get_oauth_token()

# Build PostgreSQL connection URL (using databricks_postgres database)
DATABASE_URL = (
    f"postgresql://{quote_plus(CLIENT_ID)}:{quote_plus(access_token)}"
    f"@{LAKEBASE_HOST}:{LAKEBASE_PORT}/databricks_postgres?sslmode=require"
)

# Create engine with connection pooling
engine = create_engine(
    url=DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_size=10,  # Base pool size
    max_overflow=20,  # Additional connections when pool is exhausted
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={"options": f"-c search_path={SCHEMA_NAME}"}
)

# Create session maker
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency function to get database session
    Yields session and ensures proper cleanup
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables():
    """
    Create all tables defined in ORM models
    Called on application startup
    Note: Only creates pii_details table, assessment_details already exists
    """
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create tables: {str(e)}")
        raise


def refresh_oauth_token():
    """
    Refresh OAuth token and recreate engine
    Call this periodically or when token expires
    """
    global access_token, engine, SessionLocal
    
    try:
        access_token = get_oauth_token()
        
        # Rebuild connection URL with new token
        new_database_url = (
            f"postgresql://{quote_plus(CLIENT_ID)}:{quote_plus(access_token)}"
            f"@{LAKEBASE_HOST}:{LAKEBASE_PORT}/databricks_postgres?sslmode=require"
        )
        
        # Dispose old engine
        engine.dispose()
        
        # Create new engine
        engine = create_engine(
            url=new_database_url,
            echo=False,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"options": f"-c search_path={SCHEMA_NAME}"}
        )
        
        # Recreate session maker
        SessionLocal = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
        
        logger.info("OAuth token refreshed and database connection updated")
        
    except Exception as e:
        logger.error(f"Failed to refresh OAuth token: {str(e)}")
        raise
