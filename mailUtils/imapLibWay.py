import imaplib, email, time
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('vinosambath@gmail.com', 'Vinosam12');
mail.list()

mail.select("inbox")
result, data = mail.search(None, '(UNSEEN)')

ids = data[0]
ids_list = 	ids.split()

i = -1
while(i >= -30):
	latest_email_id = ids_list[i]
	#print(mail.fetch(latest_email_id, "(RFC822)"))
	result, data = mail.fetch(latest_email_id, "(RFC822)")
	#print (data[0][1])
	typ, msg_data = mail.fetch(latest_email_id, '(RFC822)')
	for response_part in msg_data:
		if isinstance(response_part, tuple):
			msg = email.message_from_string(response_part[1])
			for header in [ 'subject', 'to', 'from' , 'date']:
				print '%-8s: %s' % (header.upper(), msg[header])

	i-=1;


	# msg_data_string = msg_data[0][1].decode('utf-8')
	# msg_data_mail = email.message_from_string(msg_data_string)

	# for part in msg_data_mail.walk():
	# 	if part.get_content_type() == "text/plain":
	# 		body = part.get_payload(decode=True)
	# 		print(body.decode('utf-8'))
