from flask import Blueprint,request,jsonify
from model.couchmodels import Response
import datetime
import logging,traceback,requests
from tasks import celery_app

response_router = Blueprint('responsehandlers',__name__)

# API for creating a response
@response_router.route('/create', methods=['POST'])
def create_response():
    response = Response()
    data = request.json
    form_id = data.get('formID',None)
    answers = data.get('answers',{})
    contact_no = data.get('Contact_No',None)

    if not form_id or not answers or not contact_no:
        return jsonify({'message': 'response_name and questions and phone no. are required'}), 400
    
    try:
        response_id = f'{form_id}_Res_{datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%SZ")}'
        response_data = {
            'Form_ID' : form_id,
            'Contact_No':contact_no,
        }

        counter = 0

        for qid,resp in answers.items():
            counter += 1
            aid = f'{response_id}_a{counter}'
            response_data[aid] = resp

            json_data = {
                'ansid' : aid,
                'qid' : qid,
                'answertext' : resp,
            }
            requests.post("http://localhost:5000/answers/create",json=json_data)
        
        
        print(response_data)
        response.model.save(response_id, response_data)
        smsdata = {
            'FormID' : form_id,
            'ResponseID' : response_id,
            'contact_no' : contact_no
        }
        celery_app.send_task('tasks.sendsms', args=(smsdata,))
        return jsonify({'message': f'response with ID {response_id} created successfully'})
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message': f'Failed to create response : {form_id}'}), 500


# API for getting a response by ID
@response_router.route('/<response_id>', methods=['GET'])
def get_response(response_id):
    response = Response().model.get(response_id)
    if response:
        return jsonify(response)
    else:
        return jsonify({'message': f'response with ID {response_id} not found'}), 404

# API for getting all responses
@response_router.route('/all', methods=['GET'])
def get_all_responses():
    try:
        responses = Response().model.get_all()
        return jsonify({'responses_list' : responses}), 200
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message': f'Failed to retrieve responses'}), 500