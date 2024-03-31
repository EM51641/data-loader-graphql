from asyncio import current_task
from typing import Callable, TypeVar, overload
from flask import Flask
from sqlalchemy import Engine, create_engine, select, Result, Function
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import Select
from flask.globals import app_ctx
from sqlalchemy.orm import Session
from db.utils import Base
import os

TEntity = TypeVar("TEntity", bound=Base)


class Database:
    """
    A class representing a database connection and operations.

    Attributes:
    ----
    _engine (Optional[Engine]): The SQLAlchemy engine.
    _session (async_scoped_session[Session]): The scoped session.

    Methods:
    ----
    __init__(): Initializes the Database object.
    session(): Returns the session object.
    engine(): Returns the engine object.
    add(entity: Base): Adds an entity to the session.
    delete(entity: Base): Deletes an entity from the session.
    commit(): Commits the changes made in the session.
    flush(): Flushes the changes made in the session.
    rollback(): Rolls back the changes made in the session.
    select(entity: type[TEntity]):
        Creates a select query for the specified entity.
    execute(query: Select[tuple[TEntity]] | Function[TEntity]):
        Executes the specified query.
    init(app: Quart): Initializes the session with the app context.
    _make_engine(): Creates the SQLAlchemy engine.
    _make_scoped_session(engine: Engine | None = None, scope_fun:
        Callable[[], int] | None = None):
        Constructs a scoped session.
    _teardown_session(exc: BaseException | None): Tears down the session.
    _get_current_context(): Returns the current app context.
    _get_current_task(): Returns the current task.
    """

    _engine: Engine | None

    def __init__(self) -> None:
        """
        Initializes a new instance of the Database class.
        """
        self._engine = None
        self._session = self._make_scoped_session()

    @property
    def session(self) -> scoped_session[Session]:
        """
        Returns the session object for interacting with the database.

        Returns:
            async_scoped_session[Session]: The session object.
        """
        return self._session

    @property
    def engine(self) -> Engine | None:
        """
        Returns the engine object used for database operations.

        Returns:
            Engine|None: The engine object used for database operations.
        """
        return self._engine

    def add(self, entity: Base) -> None:
        """
        Adds an entity to the database.

        Args:
            entity (Base): The entity to be added.

        Returns:
            None
        """
        self._session.add(entity)

    def delete(self, entity: Base) -> None:
        """
        Deletes the given entity from the database.

        Args:
            entity (Base): The entity to be deleted.

        Returns:
            None
        """
        self._session.delete(entity)

    def commit(self) -> None:
        """
        Commits the current transaction to the database.
        """
        self._session.commit()

    def flush(self) -> None:
        """
        Flushes the changes made in the session to the database.
        """
        self._session.flush()

    def rollback(self) -> None:
        """
        Rollbacks the current transaction.

        This method rolls back any changes made within the current transaction.
        """
        self._session.rollback()

    def select(self, entity: type[TEntity]) -> Select[tuple[TEntity]]:
        """
        Selects records from the database for the given entity.

        Args:
            entity (type[TEntity]): The type of entity to select records for.

        Returns:
            Select[tuple[TEntity]]:
                A query object representing the select operation.

        """
        return select(entity)

    @overload
    def execute(
        self, query: Select[tuple[TEntity]]
    ) -> Result[tuple[TEntity]]: ...  # noqa

    @overload
    def execute(self, query: Function[TEntity]) -> Result[tuple[TEntity]]: ...

    def execute(  # type: ignore
        self, query: Select[tuple[TEntity, ...]] | Function[TEntity]
    ) -> Result[tuple[TEntity, ...]]:
        res = self._session.execute(query)
        return res

    def init(self, app: Flask) -> None:
        """
        Initialise the session with the app context

        Parameters:
        ----
            app (Quart): The Quart app
        """
        self._engine = self._make_engine()
        self._session = self._make_scoped_session(
            self._engine, self._get_current_context
        )
        app.teardown_appcontext(self._teardown_session)
        app.logger.info("DB Session scoped initialised")

    def _make_engine(self) -> Engine:
        """
        Make the SQLAlchemy engine.

        Returns:
        ----
            Engine
        """
        engine = create_engine(url=os.environ["SQLALCHEMY_DATABASE_URI"])
        print(engine)
        return engine

    def _make_scoped_session(
        self,
        engine: Engine | None = None,
        scope_fun: Callable[[], int] | None = None,
    ) -> scoped_session[Session]:
        """
        Construct scoped session.

        Parameters:
        ----
            engine (Optional[Engine]): The SQLAlchemy engine

        Returns:
        ----
            async_scoped_session[Session]
        """
        if scope_fun is None:
            scope_fun = self._get_current_context

        session_maker = sessionmaker(engine, expire_on_commit=False)
        session = scoped_session(session_maker, scope_fun)
        return session

    def _teardown_session(self, exc: BaseException | None) -> None:
        """
        Tear down the session and remove it from the driver.

        Args:
            exc (BaseException | None): The exception that occurred, if any.

        Returns:
            None
        """
        self._session.remove()

    def _get_current_context(self) -> int:
        """
        Get the current context ID.

        Returns:
            int: The ID of the current context.
        """
        id_ = id(app_ctx._get_current_object())  # type: ignore
        return id_

    def _get_current_task(self) -> int:
        """
        Get the ID of the current task.

        Returns:
            int: The ID of the current task.
        """
        id_ = id(current_task())
        return id_
