from model.sqlmodels import Question,Answer,session
from celery import Celery
import logging,traceback
from SMSservice.sms import twilio_client,twilio_keys

celery_app = Celery('tasks',broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery_app.task
def create_question_task(data):
    try:
        qid = data.get('qid')
        question = data.get('question')

        if not qid or not question:
            return {'message': 'qid and text are required'}, 400

        question = Question(qid=qid, text=question)
        session.add(question)
        session.commit()

        return {'message': f'Question with ID {qid} created successfully'}
    except:
        logging.error(traceback.format_exc())
        return {'message' : f'Error occured in creating the question : {qid}'}

@celery_app.task
def create_answer_task(data):
    try:
        ansid = data.get('ansid')
        qid = data.get('qid')
        answertext = data.get('answertext')

        if not ansid or not qid or not answertext:
            return {'message': 'ansid, qid, and answertext are required'}

        answer = Answer(ansid=ansid, qid=qid, answertext=answertext)
        session.add(answer)
        session.commit()

        return {'message': f'Answer with ID {ansid} created successfully'}
    except:
        logging.error(traceback.format_exc())
        return {'message': 'Error creating new answer'}

@celery_app.task
def send_sms(data):
    ResponseID = data.get('responseID')
    FormID = data.get('FormID')
    contact_no = data.get('contact_no')
    message = twilio_client.messages.create(
        body=f"Your Response : {ResponseID} for Form : {FormID} is submitted",
        from_=twilio_keys['phone_no'],
        to=contact_no
    )

    print(f"Message SID: {message.sid}")