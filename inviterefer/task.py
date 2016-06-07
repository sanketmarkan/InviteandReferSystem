from celery.registry import tasks
from celery.task import Task
from django.core.mail import send_mail

class Sendemail(Task):

	def run(self,text,emailid):
		send_mail("New Invite",text,'sanketmarkan',[emailid,])


tasks.register(Sendemail)