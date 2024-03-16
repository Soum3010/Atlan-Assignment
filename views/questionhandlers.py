from flask import Blueprint, request, jsonify
from model.sqlmodels import Question, Answer, session
import logging,traceback
from tasks import celery_app

questions_router = Blueprint('questionhandlers', __name__)


@questions_router.route('/add', methods=['POST'])
def create_question():
    try:
        data = request.json
        print(data)
        result = celery_app.send_task('tasks.create_question_task', args=(data,))
        return jsonify({'message': f'Task added to queue. Question will be created shortly.'})
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message' : f'Error occured in creating the question.'})

@questions_router.route('/all', methods=['GET'])
def get_all_questions():
    try:
        questions = session.query(Question).all()
        questions_data = [{'qid': question.qid, 'text': question.text} for question in questions]
        return jsonify(questions_data)
    except:
        logging.error(traceback.format_exc())

@questions_router.route('/remove/<qid>', methods=['DELETE'])
def delete_question(qid):
    try:
        question = session.query(Question).filter_by(Question.qid==qid)
        if not question:
            return jsonify({'message': f'Question with ID {qid} not found'}), 404

        session.delete(session.query(Answer).filter_by(Answer.qid==qid))
        session.commit()
        session.delete(question)
        session.commit()

        return jsonify({'message': f'Question with ID {qid} and its corresponding answers deleted successfully'})
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message':f'Problem Occured in deleting question with ID {qid} and its corresponding answers'})