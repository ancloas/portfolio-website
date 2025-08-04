from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
from app.models.base import BaseModel, Base
from app.core.config import settings
from typing import List


load_dotenv()

# PostgreSQL Sync Database URL
DATABASE_URL = settings.DATABASE_URL

class DatabaseManager:
    def __init__(self, database_url: str):
        """
        Initialize the DatabaseManager with a given database URL.
        """
        self.engine = create_engine(database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self) -> None:
        """Create all tables defined in the metadata."""
        try:
            Base.metadata.create_all(self.engine)
            print('Tables created successfully.')
        except SQLAlchemyError as e:
            print(f"Error creating tables: {e}")
            raise

    def add_or_save(self, obj: BaseModel) -> None:
        """Add an ORM object to the database."""
        with self.Session() as session:
            try:
                session.add(obj)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error adding object: {e}")
                raise
    
    
    def add_or_save_multiple(self, objs: List[BaseModel]) -> None:
        """Add multiple ORM objects to the database."""
        with self.Session() as session:
            try:
                session.add_all(objs)  # Add multiple objects to the session
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error adding objects: {e}")
                raise

    def delete(self, obj: BaseModel) -> None:
        """Delete an ORM object from the database."""
        with self.Session() as session:
            try:
                session.delete(obj)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error deleting object: {e}")
                raise

    def fetch_all(self, model: BaseModel, filters: dict | None = None):
        """Fetch all objects of a specific model with optional filters."""
        with self.Session() as session:
            try:
                stmt = select(model)
                if filters:
                    for column, value in filters.items():
                        stmt = stmt.filter(getattr(model, column) == value)
                result = session.execute(stmt)
                return result.scalars().all()
            except SQLAlchemyError as e:
                print(f"Error fetching all objects: {e}")
                raise

    def fetch_one(self, model: BaseModel, filters: dict | None = None):
        """Fetch a single object of a specific model with optional filters."""
        with self.Session() as session:
            try:
                stmt = select(model)
                if filters:
                    for column, value in filters.items():
                        stmt = stmt.filter(getattr(model, column) == value)
                result = session.execute(stmt)
                return result.scalars().first()
            except SQLAlchemyError as e:
                print(f"Error fetching one object: {e}")
                raise

    def update_one_or_more(self, model: BaseModel, filters: dict, updates: dict):
        """Update one or more objects of the specified model."""
        with self.Session() as session:
            try:
                stmt = select(model).filter_by(**filters)
                result = session.execute(stmt)
                instances = result.scalars().all()

                if instances:
                    for instance in instances:
                        for key, value in updates.items():
                            setattr(instance, key, value)
                    session.add_all(instances)
                    session.commit()
                    return instances
                return []
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error updating objects: {e}")
                raise

    def execute_raw(self, query: str, params: dict | None = None):
        """Execute a raw SQL query."""
        with self.Session() as session:
            try:
                result = session.execute(text(query), params)
                session.commit()
                return result
            except SQLAlchemyError as e:
                print(f"Error executing raw query: {e}")
                raise

    def get_session(self):
        """Provide a session for direct usage."""
        session = self.Session()
        try:
            yield session
        finally:
            session.close()

# Create the database manager instance
db_manager = DatabaseManager(database_url=DATABASE_URL)
