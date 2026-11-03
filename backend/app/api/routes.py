from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db import get_db
from app.models import User, Profile, SavedWord, LearningProgress, Course, Lesson
from app.schemas import RegisterIn,LoginIn,TokenOut,UserOut,WordIn,WordOut,TutorIn,TutorOut,ProgressIn
from app.core.security import hash_password,verify_password,create_access_token
from app.dependencies import current_user,admin_user
from app.services.ai import GeminiService,AIUnavailable
router=APIRouter()
@router.post('/auth/register',response_model=UserOut,status_code=201)
def register(data:RegisterIn,db:Session=Depends(get_db)):
    if db.scalar(select(User).where(User.email==data.email.lower())): raise HTTPException(409,'Email already registered')
    user=User(email=data.email.lower(),password_hash=hash_password(data.password)); db.add(user); db.flush(); db.add(Profile(user_id=user.id,display_name=data.display_name)); db.commit(); db.refresh(user); return user
@router.post('/auth/login',response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==data.email.lower()))
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,'Incorrect email or password')
    return TokenOut(access_token=create_access_token(str(user.id),user.role))
@router.get('/auth/me',response_model=UserOut)
def me(user:User=Depends(current_user)): return user
@router.get('/languages')
def languages():
    return [{"code":c,"name":n} for c,n in [('en','English'),('ur','Urdu'),('ar','Arabic'),('hi','Hindi'),('fr','French'),('es','Spanish'),('de','German'),('it','Italian'),('pt','Portuguese'),('tr','Turkish'),('zh','Mandarin Chinese'),('ja','Japanese'),('ko','Korean'),('ru','Russian'),('nl','Dutch'),('bn','Bengali'),('id','Indonesian')]]
@router.get('/vocabulary',response_model=list[WordOut])
def words(db:Session=Depends(get_db),user:User=Depends(current_user)):
    return list(db.scalars(select(SavedWord).where(SavedWord.user_id==user.id).order_by(SavedWord.created_at.desc())))
@router.post('/vocabulary',response_model=WordOut,status_code=201)
def add_word(data:WordIn,db:Session=Depends(get_db),user:User=Depends(current_user)):
    row=SavedWord(user_id=user.id,**data.model_dump()); db.add(row)
    try: db.commit(); db.refresh(row)
    except Exception: db.rollback(); raise HTTPException(409,'This word is already saved')
    return row
@router.delete('/vocabulary/{word_id}',status_code=204)
def delete_word(word_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    row=db.scalar(select(SavedWord).where(SavedWord.id==word_id,SavedWord.user_id==user.id))
    if not row: raise HTTPException(404,'Word not found')
    db.delete(row); db.commit()
@router.post('/progress',status_code=201)
def add_progress(data:ProgressIn,db:Session=Depends(get_db),user:User=Depends(current_user)):
    row=LearningProgress(user_id=user.id,**data.model_dump()); db.add(row); db.commit(); return {"id":row.id,"saved":True}
@router.get('/progress')
def get_progress(db:Session=Depends(get_db),user:User=Depends(current_user)):
    rows=list(db.scalars(select(LearningProgress).where(LearningProgress.user_id==user.id)))
    return {"activities":len(rows),"completed":sum(x.completed for x in rows),"minutes":sum(x.minutes_spent for x in rows)}
@router.post('/ai/tutor',response_model=TutorOut)
async def tutor(data:TutorIn,user:User=Depends(current_user)):
    try:
        reply,provider=await GeminiService().tutor(data.message,data.target_language,data.known_language,data.explanation_language,data.mode)
        return TutorOut(reply=reply,provider=provider,configured=True)
    except AIUnavailable as exc: raise HTTPException(503,str(exc))
@router.get('/courses')
def courses(db:Session=Depends(get_db)):
    return [{"id":x.id,"language_code":x.language_code,"title":x.title,"level":x.level,"description":x.description} for x in db.scalars(select(Course))]
@router.get('/courses/{course_id}/lessons')
def lessons(course_id:int,db:Session=Depends(get_db)):
    if not db.get(Course,course_id): raise HTTPException(404,'Course not found')
    return [{"id":x.id,"title":x.title,"content":x.content,"order_index":x.order_index} for x in db.scalars(select(Lesson).where(Lesson.course_id==course_id).order_by(Lesson.order_index))]
@router.get('/admin/overview')
def admin_overview(db:Session=Depends(get_db),user:User=Depends(admin_user)):
    return {"users":db.scalar(select(func.count(User.id))) or 0,"courses":db.scalar(select(func.count(Course.id))) or 0,"words_saved":db.scalar(select(func.count(SavedWord.id))) or 0}

# Curriculum-backed learning endpoints. Answers are checked against authored curriculum,
# never generated or fabricated by the API.
from app.learning.catalog import load_catalog

@router.get('/learning/modules')
def learning_modules():
    return load_catalog()['modules']

@router.get('/learning/grammar')
def grammar_lessons(language_code: str = 'en'):
    return [{**x, 'question': {k: v for k, v in x['question'].items() if k != 'answer_index'}} for x in load_catalog()['grammar_lessons'] if x['language_code'] == language_code]

@router.post('/learning/grammar/{lesson_id}/check')
def check_grammar(lesson_id: str, answer_index: int):
    lesson = next((x for x in load_catalog()['grammar_lessons'] if x['id'] == lesson_id), None)
    if lesson is None:
        raise HTTPException(404, 'Grammar lesson not found')
    question = lesson['question']
    correct = answer_index == question['answer_index']
    return {'correct': correct, 'correct_answer_index': question['answer_index'], 'explanation': question['explanation']}

@router.get('/learning/reading')
def reading_passages(language_code: str = 'en'):
    return [{**x, 'questions': [{k: v for k, v in q.items() if k != 'answer_index'} for q in x['questions']]} for x in load_catalog()['reading_passages'] if x['language_code'] == language_code]

@router.post('/learning/reading/{passage_id}/check')
def check_reading(passage_id: str, question_index: int, answer_index: int):
    passage = next((x for x in load_catalog()['reading_passages'] if x['id'] == passage_id), None)
    if passage is None:
        raise HTTPException(404, 'Reading passage not found')
    if question_index < 0 or question_index >= len(passage['questions']):
        raise HTTPException(404, 'Question not found')
    question = passage['questions'][question_index]
    return {'correct': answer_index == question['answer_index'], 'correct_answer_index': question['answer_index']}
