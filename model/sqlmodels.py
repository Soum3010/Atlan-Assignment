from sqlalchemy import Column,String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import create_engine
import time

# Create a base class for our models
Base = declarative_base()

#engine = create_engine(f'mysql://{username}:{password}@{hostname}:{port}/{database_name}')
engine = create_engine('mysql://root:root@localhost:3306/atlan_task')
Session = sessionmaker(bind=engine)
session = Session()

# Define Question model
class Question(Base):
    __tablename__ = 'questions'

    qid = Column(String(45), primary_key=True)
    text = Column(String(255))

    answers = relationship("Answer", back_populates="question")

    def __repr__(self):
        return f"<Question(id={self.id}, text={self.text})>"

# Define Answer model
class Answer(Base):
    __tablename__ = 'answers'

    ansid = Column(String(225), primary_key=True)
    qid = Column(String(45), ForeignKey('questions.qid'))
    answertext = Column(String(1000))

    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer(ansid={self.ansid}, qid={self.qid}, answertext={self.answertext})>"