from manutencaoauto_api.db.extensions import db


def init_db(app, create_tables: bool = True) -> None:
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)
    if create_tables:
        with app.app_context():
            # Ensure model metadata is registered before create_all.
            import manutencaoauto_api.models  # noqa: F401
            db.create_all()
