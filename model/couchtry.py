from couchmodels import *
import datetime

date_now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%SZ")
form =  Forms()
form.model.save(date_now, {'Name':'SampleForm','Q1':'Email','Q2':'PhoneNumber'})