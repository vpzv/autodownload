#!/usr/bin/python3
import sys
import dao, boxdownload, mail, constants

sys.stdout = open("/root/autodownloadjob/schedule.mail.log", "w")

def check_if_download_complete(all_downloading, series_title):
	for download in all_downloading:
		if download['percentDone'] == 1 and download['name'].strip() == series_title.strip():
			return True
	return False


def main():
	series_inprogress = dao.find_series_inprogress()
	if not series_inprogress:
		print('No downloading series in database')
		return
	all_downloading = boxdownload.list_all()
	if not all_downloading:
		print('No downloading series in your box')
		return

	download_completed = ''
	series_to_mail = []
	for series in series_inprogress:
		if(check_if_download_complete(all_downloading, series['title'])):
			download_completed += '  ' + series['title'] + '\n'
			series_to_mail.append(series)

	# Mail completed ones
	if len(series_to_mail):
		print("Sending mail: \n%s" % download_completed)
		content = 'Hi,\n\n%d series has been downloaded to your box:\n%s\nBest Wishes,\nYour TV Box' % (len(series_to_mail), download_completed)
		if mail.send('Box download complete', content):
			for series in series_to_mail:
				dao.update_series_status(series['id'], constants.DOWLOADED_FLAG)
	else:
		print('Skip mail, since no completed series is found.')

main()
