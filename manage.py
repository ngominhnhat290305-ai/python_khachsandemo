from flask.cli import FlaskGroup

from app import create_app


def _create_app():
    return create_app()


cli = FlaskGroup(create_app=_create_app)

if __name__ == "__main__":
    cli()
