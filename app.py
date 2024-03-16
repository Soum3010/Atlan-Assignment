from flask import Flask, jsonify
from views.formhandlers import form_router
from views.questionhandlers import questions_router
from views.responsehandlers import response_router
from views.answerhandlers import answers_router
from tasks import celery_app

# Flask app
app = Flask(__name__)


app.register_blueprint(form_router,url_prefix = '/form')
app.register_blueprint(response_router,url_prefix = '/response')
app.register_blueprint(questions_router,url_prefix = '/questions')
app.register_blueprint(answers_router,url_prefix = '/answers')


@app.route('/')
def home():
    return jsonify({'status': 'Connected to the API server.'})

# Endpoint to retrieve processed messages
@app.route('/results/<task_id>')
def get_result(task_id):
    result = celery_app.AsyncResult(task_id)
    if result.ready():
        return jsonify({"status": "completed", "result": result.result})
    else:
        return jsonify({"status": "pending"})

if __name__ == '__main__':
    app.run(debug=True)
