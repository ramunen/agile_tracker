from flaskr import create_app
from flaskr.db import get_db

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert b'Add new story' in response.data
    assert b'Story one' in response.data
    assert b'Story two' in response.data

def test_create_story(client, app):
    assert client.get('/story/create').status_code == 200
    client.post('/story/create', data={'title': 'Story three', 'content': 'Some content', 'hours':3, 'minutes':50})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM stories').fetchone()[0]
        assert count == 3