#!/usr/bin/python3
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import constants

def send(title, content):
	try:
		smtpObj = smtplib.SMTP(constants.MAIL_SMTP_SERVER, constants.MAIL_SMPT_PORT)
		smtpObj.starttls()
		smtpObj.login(constants.MAIL_SMTP_USERNAME, constants.MAIL_SMTP_PASSWORD)

		corpo = MIMEText(content.encode('utf-8'), 'plain', 'utf-8')
		corpo['From'] = "From: Auto service <%s>" % constants.MAIL_SENDER
		print('To: %s' % (', '.join(constants.MAIL_RECEIVERS)))
		corpo['To'] = 'To: %s' % (', '.join(constants.MAIL_RECEIVERS))
		corpo['Subject'] = Header(title, 'utf-8')
		smtpObj.sendmail(constants.MAIL_SENDER, constants.MAIL_RECEIVERS, corpo.as_string())         
		print("Successfully send email.")
		return True
	except Exception as e:
		print("Error: unable to send email. Details: %s" % e)
		return False
