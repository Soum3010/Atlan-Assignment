from flask import Blueprint,request,jsonify
from model.couchmodels import Forms
import datetime
import logging,traceback,requests

form_router = Blueprint('formhandlers',__name__)

# API for creating a form
@form_router.route('/create', methods=['POST'])
def create_form():
    form = Forms()
    data = request.json
    form_name = data.get('form_name',None)
    questions = data.get('questions',[])

    if not form_name or not questions:
        return jsonify({'message': 'form_name and questions are required'}), 400
    
    try:
        form_id = f'{form_name}_{datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%SZ")}'
        form_data = {
            'Form_Name' : form_name,
        }

        counter = 0

        for ques in questions:
            counter += 1
            qid = f'{form_id}_q{counter}'
            form_data[qid] = ques
            #Line to send particular question using taskqueue to questions creation
            json_data = {
                'qid' : qid,
                'question' : ques
            }
            requests.post("http://localhost:5000/questions/add",json=json_data)

        
        form_data['questions'] = counter
        
        form.model.save(form_id, form_data)
        #Line to send an sms using taskqueue that form is saved

        return jsonify({'message': f'Form with ID {form_id} created successfully'})
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message': f'Failed to create form : {form_name}'}), 500


# API for getting a form by ID
@form_router.route('/<form_id>', methods=['GET'])
def get_form(form_id):
    form = Forms().model.get(form_id)
    if form:
        return jsonify(form)
    else:
        return jsonify({'message': f'Form with ID {form_id} not found'}), 404

# API for getting all forms
@form_router.route('/all', methods=['GET'])
def get_all_forms():
    try:
        forms = Forms().model.get_all()
        return jsonify({'forms_list' : forms}), 200
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message': f'Failed to retrieve forms'}), 500

# API for creating a new question in a form
@form_router.route('/<form_id>/question', methods=['POST'])
def create_form_new_question(form_id):
    try:
        data = request.json
        question_data = data.get('question_data')
        
        if not question_data:
            return jsonify({'message': 'question_id and question_data are required'}), 400
        
        form = Forms().model
        form_data = form.get(form_id)
        if not form_data:
            return jsonify({'message': f'Form with ID {form_id} not found'}), 404
        
        form_data[f'{form_id}_q{form_data["questions"]+1}'] = question_data
        form_data['questions'] = form_data['questions']+1
        form.save(form_id, form_data)
        return jsonify({'message': f'Question in {form_id} added successfully'})
    except:
        logging.error(traceback.format_exc())
        return jsonify({'message': f'Failed to add question in form : {form_id}'}), 500