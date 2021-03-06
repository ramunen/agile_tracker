from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.db import get_db, get_task, get_devs, get_task_logs

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

@bp.route('/<int:task_id>/view', methods=('GET', 'POST'))
def view_task(task_id):
    
    task = get_task(task_id)
    logs = get_task_logs(task_id)
    
    return render_template('task/view.html', task_id=task_id, task=task, logs=logs)


@bp.route('/<int:task_id>/update', methods=('GET', 'POST'))
def update_task(task_id):
    task = get_task(task_id)

    dev_names = [dev['name_surname'] for dev in get_devs()]
    estimate = task['estimate'] if task['estimate'] is not None else 0
    hours_db = estimate // 60
    minutes_db = estimate % 60 

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
                'UPDATE tasks SET developer_id = ?, title = ?, content = ?, estimate = ?, iteration = ?'
                ' WHERE id = ?',
                (developer_id, title, content, estimate, iteration, task_id)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('task/update.html', task=task, developers=dev_names, hours=hours_db, minutes=minutes_db)

@bp.route('/<int:task_id>/delete', methods=('POST',))
def delete_task(task_id):
    get_task(task_id)
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    return redirect(url_for('index'))