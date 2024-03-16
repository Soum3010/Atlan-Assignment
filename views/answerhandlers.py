from flask import Blueprint, request, jsonify
from model.sqlmodels import Answer, session
import logging,traceback
from tasks import celery_app


answers_router = Blueprint('answerhandlers',__name__)

@answers_router.route('/create', methods=['POST'])
def create_answer():
    try:
        data = request.json
        result = celery_app.send_task('tasks.create_answer_task' , args=(data,))
        return jsonify({'message': f'Task added to queue. Answer will be created shortly.'})
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message': 'Error creating new answer'}), 500


@answers_router.route('/<qid>', methods=['GET'])
def get_answers_by_qid(qid):
    try:
        answers = session.query(Answer).filter_by(Answer.qid==qid).all()

        if not answers:
            return jsonify({'message': 'No answers found for the given qid'}), 404

        answers_data = [{'ansid': answer.ansid, 'answertext': answer.answertext} for answer in answers]
        return jsonify(answers_data)
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message': f'Error retrieving answers by {qid}'}), 500