from sqlalchemy import event

from manutencaoauto_api.db.extensions import db


_REGISTERED_SQLITE_ENGINES: set[int] = set()


def _set_sqlite_fk_pragma(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def _enable_sqlite_foreign_keys() -> None:
    engine = db.engine
    if engine.dialect.name != "sqlite":
        return

    engine_key = id(engine)
    if engine_key in _REGISTERED_SQLITE_ENGINES:
        return

    event.listen(engine, "connect", _set_sqlite_fk_pragma)
    _REGISTERED_SQLITE_ENGINES.add(engine_key)

    # Enforce FK checks for the current connection immediately.
    with engine.connect() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")


def init_db(app, create_tables: bool = True) -> None:
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)
    with app.app_context():
        _enable_sqlite_foreign_keys()
        if create_tables:
            # Ensure model metadata is registered before create_all.
            import manutencaoauto_api.models  # noqa: F401
            db.create_all()
