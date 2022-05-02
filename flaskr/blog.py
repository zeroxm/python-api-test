"""blog functions"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from psycopg2.extras import RealDictCursor

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """index route"""
    pg_db = get_db()
    cursor = pg_db.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN usuario u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )

    posts = cursor.fetchall()

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            pg_db = get_db()
            pg_db.cursor().execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            pg_db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(user_id, check_author=True):
    cursor = get_db().cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN usuario u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (user_id,)
    )

    post = cursor.fetchone()

    if post is None:
        abort(404, f"Post id {user_id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:user_id>/update', methods=('GET', 'POST'))
@login_required
def update(user_id):
    post = get_post(user_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            pg_db = get_db()

            pg_db.cursor().execute(
                'UPDATE post SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, user_id)
            )
            pg_db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:user_id>/delete', methods=('POST',))
@login_required
def delete(user_id):
    get_post(user_id)
    pg_db = get_db()
    pg_db.cursor().execute('DELETE FROM post WHERE id = %s', (user_id,))
    pg_db.commit()
    return redirect(url_for('blog.index'))
