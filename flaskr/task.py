from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.db import get_db, get_devs

bp = Blueprint('task', __name__, url_prefix='/task')

@bp.route('/create', methods=('GET', 'POST'))
def create_task():
    story_id = request.args.get('story_id')

    story = get_db().execute(
        'SELECT id, title, content FROM stories WHERE id = ?', (story_id,)).fetchone()
    
    dev_names = [dev['name_surname'] for dev in get_devs()]
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        estimate = int(hours*60 + minutes)
        iteration = request.form['iteration']
        developer_name = request.form['developer']
        
        developer_id = dev_names.index(request.form['developer'])+1 if developer_name in dev_names else ''
        
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tasks (developer_id, story_id, title, content, estimate, iteration)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (developer_id, story_id, title, content, estimate, iteration, )
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('task/create.html', story_id=story_id, story=story, developers=dev_names)

def get_task(task_id):
    task = get_db().execute(
        'SELECT id, developer_id, story_id, title, content, estimate, iteration FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if task is None:
        abort(404, f"Story {task_id} doesn't exist.")

    return task

@bp.route('/<int:task_id>/update', methods=('GET', 'POST'))
def update_task(task_id, developers):
    task = get_task(task_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        hours = request.form['hours']
        minutes = request.form['minutes']
        estimate = hours*60 + minutes
        iteration = request.form['iteration']
        developer_id = request.form['developer_id']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE tasks SET developer_id = ?, title = ?, content = ?, estimate = ?, iteration = ?'
                ' WHERE id = ?',
                (developer_id, title, content, estimate, iteration, task_id)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('task/update.html', task=task, developers=developers)

@bp.route('/<int:task_id>/delete', methods=('POST',))
def delete_task(task_id):
    get_task(task_id)
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    return redirect(url_for('index'))