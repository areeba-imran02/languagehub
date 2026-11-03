import os, tempfile
os.environ['DATABASE_URL']='sqlite://'
os.environ['SECRET_KEY']='test-secret-key-for-tests-only'
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.db import Base,engine
Base.metadata.create_all(bind=engine)
client=TestClient(app)
@pytest.fixture(autouse=True)
def reset_db():
 Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)
def register(email='learner@example.com'):
 return client.post('/api/v1/auth/register',json={'email':email,'password':'strong-password-123','display_name':'Learner'})
def token():
 register(); r=client.post('/api/v1/auth/login',json={'email':'learner@example.com','password':'strong-password-123'}); return r.json()['access_token']
def test_health(): assert client.get('/health').json()['status']=='ok'
def test_register_login_and_me():
 r=register(); assert r.status_code==201
 t=client.post('/api/v1/auth/login',json={'email':'learner@example.com','password':'strong-password-123'}); assert t.status_code==200
 me=client.get('/api/v1/auth/me',headers={'Authorization':'Bearer '+t.json()['access_token']}); assert me.json()['email']=='learner@example.com'
def test_user_vocabulary_is_persisted():
 headers={'Authorization':'Bearer '+token()}
 r=client.post('/api/v1/vocabulary',headers=headers,json={'word':'سلام','translation':'hello','language_code':'ur'}); assert r.status_code==201
 assert client.get('/api/v1/vocabulary',headers=headers).json()[0]['word']=='سلام'
def test_ai_missing_key_is_explicit():
 headers={'Authorization':'Bearer '+token()}
 r=client.post('/api/v1/ai/tutor',headers=headers,json={'message':'Teach me','target_language':'ur','known_language':'en','explanation_language':'en','mode':'fast'})
 assert r.status_code in (200,503)
def test_unauthenticated_vocabulary_rejected(): assert client.get('/api/v1/vocabulary').status_code==401

def test_curriculum_modules_and_grammar_check():
    modules = client.get('/api/v1/learning/modules')
    assert modules.status_code == 200
    assert {'grammar', 'reading', 'writing'} <= {x['id'] for x in modules.json()}
    lessons = client.get('/api/v1/learning/grammar?language_code=en')
    assert lessons.status_code == 200 and lessons.json()
    lesson_id = lessons.json()[0]['id']
    result = client.post(f'/api/v1/learning/grammar/{lesson_id}/check?answer_index=1')
    assert result.status_code == 200
    assert result.json()['correct'] is True

def test_reading_comprehension_check():
    passages = client.get('/api/v1/learning/reading?language_code=en')
    assert passages.status_code == 200 and passages.json()
    passage = passages.json()[0]
    result = client.post(f"/api/v1/learning/reading/{passage['id']}/check?question_index=0&answer_index=1")
    assert result.status_code == 200
    assert result.json()['correct'] is True


def test_learning_catalog_does_not_expose_answer_keys():
    grammar = client.get('/api/v1/learning/grammar?language_code=en').json()
    reading = client.get('/api/v1/learning/reading?language_code=en').json()
    assert grammar and 'answer_index' not in grammar[0]['question']
    assert reading and all('answer_index' not in q for q in reading[0]['questions'])

def test_progress_rejects_negative_minutes_and_out_of_range_scores():
    headers = {'Authorization': 'Bearer ' + token()}
    bad_minutes = client.post('/api/v1/progress', headers=headers, json={
        'activity_type': 'lesson', 'minutes_spent': -1
    })
    bad_score = client.post('/api/v1/progress', headers=headers, json={
        'activity_type': 'quiz', 'score': 101
    })
    assert bad_minutes.status_code == 422
    assert bad_score.status_code == 422

def test_progress_summary_is_scoped_to_signed_in_user():
    headers = {'Authorization': 'Bearer ' + token()}
    saved = client.post('/api/v1/progress', headers=headers, json={
        'activity_type': 'grammar', 'activity_id': 'present-simple',
        'completed': True, 'score': 90, 'minutes_spent': 12
    })
    assert saved.status_code == 201
    summary = client.get('/api/v1/progress', headers=headers)
    assert summary.json() == {'activities': 1, 'completed': 1, 'minutes': 12}
