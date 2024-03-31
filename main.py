"""
The main entry point for the application.
"""

from flask import Flask
from db.extension import db
from schemas.view import view_func
from dotenv import load_dotenv
from db.tables import BaseEntity  # noqa

load_dotenv()


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    db.init(app)
    BaseEntity.metadata.create_all(bind=db.engine)  # type: ignore
    app.add_url_rule("/graphql", view_func=view_func)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
