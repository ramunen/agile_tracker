import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    developers = [(['John Smith']), (['Janne Jalonen']), (['Anna Teesti']), (['James Joyce'])]
    db.executemany(
        'INSERT INTO developers (name_surname)'
        ' VALUES (?)', developers)
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_devs():
    db = get_db()
    devs = db.execute('SELECT id, name_surname FROM developers ORDER BY id ASC').fetchall()

    return devs

def get_stories():
    db = get_db()
    stories = db.execute('SELECT id, title, content, estimate FROM stories ORDER BY id ASC').fetchall()
    
    return stories

def get_all_tasks():
    db = get_db()
    tasks = db.execute('SELECT s.id, s.title, t.id, t.title, t.content, t.estimate, d.id, d.name_surname FROM tasks t \
            JOIN stories s ON s.id = t.story_id \
            JOIN developers d ON d.id = t.developer_id \
            ORDER BY t.id ASC').fetchall()
    
    return tasks

def get_story_tasks(story_id):
    db = get_db()
    tasks = db.execute('SELECT s.id, s.title, t.id, t.title, t.content, t.iteration, t.estimate, d.id, d.name_surname FROM tasks t \
            JOIN stories s ON s.id = t.story_id \
            LEFT JOIN developers d ON d.id = t.developer_id \
            WHERE s.id = ? \
            ORDER BY t.id ASC', (story_id,)).fetchall()
    
    return tasks

def get_task_logs(task_id):
    db = get_db()
    tasks = db.execute('SELECT t.id, t.title, l.id, l.content, l.actual, d.id, d.name_surname FROM logs l \
            JOIN tasks t ON t.id = l.task_id \
            JOIN developers d ON d.id = t.developer_id \
            WHERE t.id = ? \
            ORDER BY l.id ASC', (task_id,)).fetchall()
    
    return tasks