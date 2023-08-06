"""Easy access to postgres databases via psycopg2"""

import contextlib
import typing
import mara_db.dbs


@contextlib.contextmanager
def postgres_cursor_context(db: typing.Union[str, mara_db.dbs.PostgreSQLDB]) -> 'psycopg2.extensions.cursor':
    """Creates a context with a psycopg2 cursor for a database alias"""
    import psycopg2
    import psycopg2.extensions

    if isinstance(db, str):
        db = mara_db.dbs.db(db)

    assert (isinstance(db, mara_db.dbs.PostgreSQLDB))
    connection = psycopg2.connect(dbname=db.database, user=db.user, password=db.password,
                                  host=db.host, port=db.port)  # type: psycopg2.extensions.connection
    cursor = connection.cursor()  # type: psycopg2.extensions.cursor
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
