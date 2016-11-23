#!/usr/bin/python3
import sys, os, html, http.cookiejar, socket, urllib, httplib2, json, codecs, time, sqlite3,re
import constants
from unidecode import unidecode

def find_box_http_header():
	http = httplib2.Http()
	try:
		response = http.request(constants.BOX_SUBMIT_ADDRESS, 'POST', body={})
		return {'X-Transmission-Session-Id':response[0]['x-transmission-session-id'], 'Content-Type':'application/json'}
	except:
		print('Failed to connect box')
		return None


def send_download_link_to_box(headers, download_link):
	form_data = json.dumps({"method":"torrent-add","arguments":{"paused":"false","download-dir":"/mnt/usbhost/Storage01/download","filename":download_link}})
	try:
		http = httplib2.Http()
		response = http.request(constants.BOX_SUBMIT_ADDRESS, 'POST', headers=headers, body=form_data)
		if 'success' in str(response):
			if 'torrent-duplicate' in str(response):
				print("   WARN: duplicated")
			return True
		else:
			print(response)
			return False
	except httplib2.ServerNotFoundError as e:
		print('   ERROR: %s' % e)
		return False
	return True


def send_download_link(download_link):
	send_download_link_to_box(find_box_http_header(), download_link)


# JSON array format: {'percentDone': 1, 'name': 'Westworld.S01E05.HDTVrip.1024X576.mp4', 'id': 1}
def list_all():
	headers = find_box_http_header()
	if not headers:
		return None

	form_data = json.dumps({"method":"torrent-get","arguments":{"fields":["id","name","percentDone"]}})
	http = httplib2.Http()
	try:
		response, content = http.request(constants.BOX_SUBMIT_ADDRESS, 'POST', headers=headers, body=form_data)
		return json.loads(str(content, 'unicode-escape'))['arguments']['torrents']
	except socket.error as e:
		print('Cannot connect to box: %s' % e)
		return None
