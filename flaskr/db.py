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

def get_task(task_id):
    db = get_db()
    task = db.execute('SELECT t.id as id, t.developer_id as developer_id, d.name_surname as developer_name, t.story_id as story_id, s.title as story_title, t.title as title, t.content as content, t.estimate as estimate, sum(l.actual) as actual, t.iteration as iteration FROM tasks t \
            JOIN stories s ON s.id = t.story_id \
            LEFT JOIN developers d ON d.id = t.developer_id \
            LEFT JOIN logs l ON l.task_id = t.id \
            WHERE t.id = ? \
            GROUP BY t.id', (task_id,)).fetchone()

    return task

def get_all_tasks():
    db = get_db()
    tasks = db.execute('SELECT s.id as story_id, s.title as story_title, t.id as task_id, t.title as task_title, t.content as task_content, t.iteration as task_iteration, t.estimate as task_estimate, d.id as developer_id, d.name_surname as developer_name FROM tasks t \
            JOIN stories s ON s.id = t.story_id \
            LEFT JOIN developers d ON d.id = t.developer_id \
            ORDER BY t.id ASC').fetchall()
    
    return tasks

def get_story_tasks(story_id):
    db = get_db()
    tasks = db.execute('SELECT s.id as story_id, s.title as story_title, t.id as task_id, t.title as task_title, t.content as task_content, t.iteration as task_iteration, t.estimate as task_estimate, sum(l.actual) as task_actual, d.id as developer_id, d.name_surname as developer_name FROM tasks t \
            JOIN stories s ON s.id = t.story_id \
            LEFT JOIN developers d ON d.id = t.developer_id \
            LEFT JOIN logs l ON l.task_id = t.id \
            WHERE s.id = ? \
            GROUP BY t.id ORDER BY t.id ASC', (story_id,)).fetchall()

    return tasks

def get_task_logs(task_id):
    db = get_db()
    logs = db.execute('SELECT t.id as task_id, t.title as task_title, l.id as log_id, l.work_date as work_date, l.content as log_content, l.actual as log_actual, d.id as developer_id, d.name_surname as developer_name FROM logs l \
            JOIN tasks t ON t.id = l.task_id \
            LEFT JOIN developers d ON d.id = t.developer_id \
            WHERE t.id = ? \
            ORDER BY l.id ASC', (task_id,)).fetchall()
    
    return logs