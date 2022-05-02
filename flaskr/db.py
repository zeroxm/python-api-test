import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host="localhost",
            database="python_test",
            user="postgres",
            password="")

    return g.db


def close_db(env=None):
    pg_db = g.pop('db', None)

    if pg_db is not None:
        pg_db.close()


def init_db():
    pg_db = get_db()

    with current_app.open_resource('schema.sql') as sql_file:
        statement = sql_file.read().decode('utf8')
        try:
            pg_db.cursor().execute(f'{statement}')
            pg_db.commit()
        except psycopg2.Error as error_msg:
            print(error_msg)
            pg_db.rollback()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
