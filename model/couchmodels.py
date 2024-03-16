from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions
from couchbase.exceptions import  CouchbaseException

class CouchModel:
    def __init__(self, bucket):
        self.authenticator = PasswordAuthenticator('playstore_app', 'playstore_app')
        self.couch_cluster = Cluster('couchbase://localhost', ClusterOptions(self.authenticator))
        self.bucket = self.couch_cluster.bucket(bucket)
        self.bucket_name = bucket

    def save(self, key, data):
        try:
            self.bucket.default_collection().upsert(key, data)
            return True
        except CouchbaseException as e:
            print(f"Failed to save document: {e}")
            return False

    def get(self, key):
        try:
            return self.bucket.default_collection().get(key).content
        except CouchbaseException as e:
            print(f"Failed to get document: {e}")
            return None

    def delete(self, key):
        try:
            self.bucket.default_collection().remove(key)
            return True
        except CouchbaseException as e:
            print(f"Failed to delete document: {e}")
            return False
    
    def get_all(self):
        try:
            forms = []
            for result in self.couch_cluster.query(f'SELECT * FROM {self.bucket_name}'):
                forms.append(result)
            return forms
        except CouchbaseException as e:
            print(f"Failed to get all forms: {e}")
            return None

class Forms:
    '''
        Arguments:-
        1. formId : Unique id for the form (String).
        2. Name : Title of the Form.
        3. Questions: question numbers associated with the Form.
    '''
    def __init__(self):
        self.model=CouchModel("Forms")

class Response:
    '''
        Arguments:- 
        1. formId : Id of the form which this response is related to.
        2. ResponseId : Id of the resonse created.
        3. Answers: A list of a pair of question_id and answers to corresponding questions.
    '''
    def __init__(self):
        self.model  = CouchModel('Response')