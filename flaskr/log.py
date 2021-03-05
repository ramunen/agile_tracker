from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('log', __name__, url_prefix='/log')

@bp.route('/log', methods=('GET', 'POST'))
def create_log():
    task_id = request.args.get('task_id')

    task = get_db().execute(
        'SELECT id, title, content, developer_id FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if request.method == 'POST':
        content = request.form['content']
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        actual = int(hours*60 + minutes)
        developer_id = task['developer_id']
        error = None

        if not actual:
            error = 'Time is required.'

        if not developer_id:
            error = 'Selecting developer is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'INSERT INTO logs (developer_id, task_id, content, actual)'
                ' VALUES (?, ?, ?, ?)',
                (developer_id, task_id, content, actual, )
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('log/create.html', task_id=task_id, task=task)

def get_log(log_id):
    log = get_db().execute(
        'SELECT id, developer_id, task_id, content, actual FROM logs WHERE id = ?', (log_id,)).fetchone()

    if log is None:
        abort(404, f"Story {log_id} doesn't exist.")

    return log

@bp.route('/<int:log_id>/update', methods=('GET', 'POST'))
def update_log(log_id, developers):
    log = get_log(log_id)

    if request.method == 'POST':
        content = request.form['content']
        hours = request.form['hours']
        minutes = request.form['minutes']
        actual = hours*60 + minutes
        developer_id = request.form['developer_id']
        error = None

        if not actual:
            error = 'Time is required.'

        if not developer_id:
            error = 'Selecting developer is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE logs SET developer_id = ?, content = ?, actual = ?'
                ' WHERE id = ?',
                (developer_id, content, actual, log_id)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('log/update.html', log=log, developers=developers)

@bp.route('/<int:log_id>/delete', methods=('POST',))
def delete_log(log_id):
    get_log(log_id)
    db = get_db()
    db.execute('DELETE FROM logs WHERE id = ?', (log_id,))
    db.commit()
    return redirect(url_for('index'))