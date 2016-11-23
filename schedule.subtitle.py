#!/usr/bin/python3
import sys, os, http.cookiejar, socket, urllib, httplib2, json, codecs, time, sqlite3, re, zipfile
from bs4 import BeautifulSoup
import constants, boxdownload, zimuzu


def download_to_box(tv_name, download_link):
	temp_file_name = "%s.%s" % (tv_name, download_link.split(".")[-1])
	urllib.request.urlretrieve(download_link, temp_file_name)
	zip_ref = zipfile.ZipFile(temp_file_name, 'r')
	zip_ref.extractall(constants.TEMP_FOLDER)
	zip_ref.close()

	sub_folders = [name for name in os.listdir(constants.TEMP_FOLDER)
		if os.path.isdir(os.path.join(constants.TEMP_FOLDER, name))]
	search_bt_file_name = sub_folders[0]
	print('File name:%s' % search_bt_file_name)

	video_download_link = ''
	http = httplib2.Http()
	try:
		response, content = http.request('https://thepiratebay.org/search/%s/0/99/0' % search_bt_file_name, 'GET')
		result_page =  BeautifulSoup(content, 'html.parser')
		for link in result_page.find_all(href=re.compile('^magnet.*')):
			video_download_link = link['href']
			break
	except socket.error as e:
		print('Cannot connect to box: %s' % e)
		return

	print('Video download: %s' % video_download_link)
	boxdownload.send_download_link(video_download_link)


def main():
	tv_name='The big bang theory S10E08'
	link = zimuzu.fetch_subtitle_download_link(tv_name)
	if not link:
		return

	print('%s:\nSubtitle:%s' % (tv_name,link))

	if not os.path.exists(constants.TEMP_FOLDER):
		os.makedirs(constants.TEMP_FOLDER)

	download_to_box(tv_name, link)


main()
