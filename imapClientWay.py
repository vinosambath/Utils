import imapclient, pyzmail
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login('*', '*')

imapObj.select_folder('INBOX', readonly=True)
UIDs = imapObj.search([u'SINCE', date(2016, 12, 23)])

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
	print(_from)
	if isinstance(_from, list):
		print _from
		if _from[0][1]  in fromHash:
			print "yes"
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
MESSAGE['To'] = "*"
MESSAGE['From'] = "*"
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
password = "Vinosam12"

server.starttls()
server.login("*", "*")
server.sendmail("*", ["*"], MESSAGE.as_string())
server.quit()

# part2 = MIMEText(s, 'html')
# print(smtpObj.sendmail('vinosambath@gmail.com', 'vinosambath@gmail.com', s))
# smtpObj.quit()