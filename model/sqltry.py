from sqlmodels  import *

#First time to create the required tables
Base.metadata.create_all(engine)

#create
question1 = Question(qid='aq1', text='What is the capital of France?')
question2 = Question(qid='bq1', text='Where should I go?')

session.add(question1)
session.add(question2)
session.commit()
time.sleep(30)


#read
all_questions = session.query(Question).all()
for question in all_questions:
    print(question.qid, question.text)

#Update and delete
question_id1 = 'aq1'
question_id2 = 'bq1'
ques1 = session.query(Question).filter(Question.qid==question_id1).first()
ques2 = session.query(Question).filter(Question.qid==question_id2).first()

if ques1:
    ques1.text = 'Ok updated Question?'
    session.commit()

if ques2:
    session.delete(ques2)
    session.commit()