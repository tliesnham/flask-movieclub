import pytest
from movieclub.db import get_db

def test_index(client, auth):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Sign Up' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'Add Movie' in response.data


def test_pagination(client):
    response = client.get('/?p=2')
    assert response.status_code == 404

    response = client.get('/?p=1')
    assert response.status_code == 200


@pytest.mark.parametrize('path', (
    '/create',
    '/1',
))
def test_login_required(client, path):
    if path == '/1':
        response = client.post(path, data={'rating': 5})
        assert b'Please login to rate this movie.' in response.data
    else:
        response = client.post(path)
        assert response.headers['Location'] == 'http://localhost/auth/login'


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'synopsis': 'Synopsis', 'age_rating': 'U', 'release_year': 2000})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM movie').fetchone()[0]
        assert count == 2


@pytest.mark.parametrize(('title', 'synopsis', 'release_year', 'age_rating',
        'message'), (
    ('', '', '', '', b'Title is required.'),
    ('a', '', 2000, '', b'Synopsis is required.'),
    ('a', 'test', '', '', b'Release year is required.'),
    ('a', 'test', 2000, '', b'Age rating required.'),
))
def test_create_validate(client, auth, title, synopsis, release_year,
        age_rating, message):
    auth.login()
    response = client.post('/create', data={
        'title': title,
        'synopsis': synopsis,
        'release_year': release_year,
        'age_rating': age_rating
    })

    assert message in response.data


def test_view(client):
    response = client.get('/1')
    assert response.status_code == 200

    response = client.get('/3')
    assert response.status_code == 404


def test_view_rating(client, auth):
    auth.login()
    response = client.post('/1', data={'rating': 10})
    assert b'Please choose a rating from 1-5.' in response.data

    response = client.post('/1', data={'rating': 5})
    assert b'Thank you for your rating.' in response.data

    response = client.post('/1', data={'rating': 1})
    assert b'You have already rated this movie.' in response.data
