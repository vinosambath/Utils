from __future__ import absolute_import, unicode_literals
from datetime import timedelta
import imapclient, pyzmail
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import pymongo
from celery import Celery
from celery.schedules import crontab 

from pymongo import MongoClient
client = MongoClient()

db = client.test

logging.basicConfig()
#sched = BackgroundScheduler()

app = Celery()
app.conf.update(
	BROKER_URL='redis://localhost',
	CELERYBEAT_SCHEDULE = {
	'every-minute': {
		'task': 'mail',
		'schedule':crontab(minute='*/1'),
		},
	}
)



@app.task(name='mail')
def mail():
	print("in")
	imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
	imapObj.login('fakegithub@gmail.com', 'fakeyou1')

	imapObj.select_folder('INBOX', readonly=True)
	UIDs = imapObj.search([u'SINCE', date(2016, 12, 22)])

	fromHash = {}

	for uid in UIDs:
		rawMessages = imapObj.fetch([uid], [b'BODY[]', 'FLAGS'])
		message = pyzmail.PyzMessage.factory(rawMessages[uid][b'BODY[]'])
		_from = message.get_addresses('from')
		_to = message.get_addresses('to')
		_cc = message.get_addresses('cc')
		_bcc = message.get_addresses('bcc')
		_text = None
		_htmlText = None
		if(message.text_part != None and message.text_part.charset != None):
			_text = message.text_part.get_payload().decode(message.text_part.charset)
		if(message.html_part != None):
			_htmlText = message.html_part.get_payload().decode(message.html_part.charset)
		if isinstance(_from, list):
			#print _from
			if _from[0][1]  in fromHash:
				#print "yes"
				fromHash[_from[0][1]] += 1
			else:
				fromHash[_from[0][1]] = 1
		else:
			if _from in fromHash:
				fromHash[_from] += 1
			else:
				fromHash[_from] = 1

	MESSAGE = MIMEMultipart('alternative')
	MESSAGE['subject'] = "mimetext example"
	MESSAGE['To'] = "fakegithub@gmail.com"
	MESSAGE['From'] = "fakegithub@gmail.com"
	MESSAGE.preamble = ""

	s = ""
	s += "<table>"
	s += "<tr>"
	s += "<th> from </th>"
	s += "<th> Count </th>"
	s += "</tr>"
	for key in fromHash:
		s += "<tr>"
		s += "<th>" + key + "</th>" + "<th>" + str(fromHash[key]) + "</th>"
		s += "</tr>"

	HTML_BODY = MIMEText(s, 'html')
	MESSAGE.attach(HTML_BODY)
	server = smtplib.SMTP('smtp.gmail.com:587')

	server.starttls()
	server.login("fakegithub@gmail.com", "fakeyou1")
	server.sendmail("fakegithub@gmail.com", ["fakegithub@gmail.com"], MESSAGE.as_string())
	server.quit()

	# part2 = MIMEText(s, 'html')
	# print(smtpObj.sendmail('vinosambath@gmail.com', 'vinosambath@gmail.com', s))
	# smtpObj.quit()
# job = sched.add_job(mail, 'interval', minutes=1, id="vinosambath@gmail.com")
# print job

# # db = client.test
# # collection = db['mailStat']


# # result = db.mailStat.insert_one({"mail":"fakegithub@gmail.com", "password":"fakeyou1", "job": job})
# # print(result.inserted_id)
# sched.start()