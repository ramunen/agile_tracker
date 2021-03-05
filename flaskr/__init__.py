import os

from flask import Flask, render_template
from flaskr.db import get_db, get_stories, get_story_tasks

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
     
 
    from . import db
    db.init_app(app)

    @app.route('/index')
    def index():
        
        stories = get_stories()
        story_tasks = {}
        for story in stories:
            
            story_tasks[story['id']] = get_story_tasks(story['id'])
            
        return render_template('/index.html', stories=stories, story_tasks=story_tasks)

    from . import story
    app.register_blueprint(story.bp)
    #app.add_url_rule('/', endpoint='story')

    from . import task
    app.register_blueprint(task.bp)
    #app.add_url_rule('/', endpoint='task')

    from . import log
    app.register_blueprint(log.bp)
    #app.add_url_rule('/', endpoint='log')

    return app