from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.db import get_db, get_story_tasks, get_task_logs

bp = Blueprint('story', __name__, url_prefix='/story')

@bp.route('/create', methods=('GET', 'POST'))
def create_story():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        estimate = int(hours*60 + minutes)
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO stories (title, content, estimate)'
                ' VALUES (?, ?, ?)',
                (title, content, estimate)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('story/create.html')

def get_story(story_id):
    story = get_db().execute(
        'SELECT id, title, content, estimate FROM stories s WHERE s.id = ?', (story_id,)).fetchone()

    if story is None:
        abort(404, f"Story {story_id} doesn't exist.")

    return story

@bp.route('/<int:story_id>/view', methods=('GET', 'POST'))
def view_story(story_id):
    #story_id = request.args.get('story_id')

    story = get_story(story_id)
    
    tasks = get_story_tasks(story_id)
    
    logs = {}
    story_logged_hours = 0
    for task in tasks:
        logs[task['task_id']] = get_task_logs(task['task_id'])
        story_logged_hours += task['task_actual'] if task['task_actual'] is not None else 0
        
    return render_template('story/view.html', story_id=story_id, story=story, tasks=tasks, logs=logs, story_logged_hours=story_logged_hours)

@bp.route('/<int:story_id>/update', methods=('GET', 'POST'))
def update_story(story_id):
    story = get_story(story_id)
    estimate = story['estimate'] if story['estimate'] is not None else 0
    hours_db = estimate // 60
    minutes_db = estimate % 60 

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        hours = request.form['hours']
        minutes = request.form['minutes']
        estimate = hours*60 + minutes
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE stories SET title = ?, content = ?, estimate = ?'
                ' WHERE id = ?',
                (title, content, estimate, story_id)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('story/update.html', story_id=story_id, story=story, hours=hours_db, minutes=minutes_db)

@bp.route('/<int:story_id>/delete', methods=('POST',))
def delete_story(story_id):
    #get_story(story_id)
    db = get_db()
    db.execute('DELETE FROM stories WHERE id = ?', (story_id,))
    db.commit()
    return redirect(url_for('index'))
