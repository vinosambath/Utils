import imapclient, pyzmail
from datetime import date
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login('vinosambath@gmail.com', '*')

imapObj.select_folder('INBOX', readonly=True)
UIDs = imapObj.search([u'SINCE', date(2016, 12, 17)])
print (UIDs)

for uid in UIDs:
	rawMessages = imapObj.fetch([uid], [b'BODY[]', 'FLAGS'])
	message = pyzmail.PyzMessage.factory(rawMessages[uid][b'BODY[]'])
	print(message.get_addresses('from'))
	print(message.get_addresses('to'))
	print(message.get_addresses('cc'))
	print(message.get_addresses('bcc'))
	#print(message.text_part.get_payload().decode(message.text_part.charset))
	#print(message.html_part.get_payload().decode(message.html_part.charset))