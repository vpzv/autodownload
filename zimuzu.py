#!/usr/bin/python3
import sys, os, http.cookiejar, socket, urllib, httplib2, json, codecs, time, sqlite3, re, zipfile
import constants
from bs4 import BeautifulSoup, SoupStrainer


def login_zimuzu():
	cj = http.cookiejar.MozillaCookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	login_data = urllib.parse.urlencode({'account': constants.ZIMUZU_LOGIN_USERNAME, 'password': constants.ZIMUZU_LOGIN_PASSWORD, 'remember': 1}).encode("utf-8")
	try:
		response = opener.open('http://www.zimuzu.tv/User/Login/ajaxLogin', login_data, timeout = constants.WEB_CONNECT_TIMEOUT)
		response_text=str(response.read(), 'unicode-escape')
		if not 'status' in response_text or not '登录成功' in response_text:
			print(response_text)
			return None
	except urllib.error.HTTPError as e:
		print('Cannot connect to %s: %s' % (constants.ZIMUZU_NAME, e))
		return None
	except socket.timeout:
		print(' Connect to %s timeout' % constants.ZIMUZU_NAME)
		return None
	return opener


def fetch_all_series_for_zimuzu(tv):
	opener = login_zimuzu()
	if not opener:
		return None
	try:
		page = opener.open(tv['url'], timeout=constants.WEB_CONNECT_TIMEOUT).read().decode('utf-8')
	except socket.timeout:
		print(' Error: Connect to %s timeout' % constants.ZIMUZU_NAME)
		return None

	result_page = BeautifulSoup(page, 'html.parser')
	response_json = []
	for link in result_page.find_all(attrs={"type": "magnet"}):
		title = link.find_next_sibling('a').get('thunderrestitle')
		magnet = link.get('href')
		if title and '中英' in title and magnet:
			response_json.append({"title": title, "link": magnet})
	print(' %s episodes found' % str(len(response_json)))
	return response_json


def fetch_subtitle_download_link(tv_name):
	http = httplib2.Http()
	try:
		response, content = http.request('http://www.zimuzu.tv/search/api?%s&type=' % urllib.parse.urlencode({'keyword':tv_name}), 'GET')
		response_json = json.loads(str(content, 'unicode-escape'))['data']
		if not response_json:
			return None

		response, content = http.request('http://www.zimuzu.tv/subtitle/%s' % response_json[0]['itemid'], 'GET')
		result_page =  BeautifulSoup(content, 'html.parser')
		for link in result_page.find_all(href=re.compile('.*\.(zip|rar|7z)$')):
			if link.has_attr('href') and (link['href'].endswith('.zip') or link['href'].endswith('.rar') or link['href'].endswith('.7z')):
				return link['href']
		return None
	except socket.error as e:
		print('Cannot connect to box: %s' % e)
		return None

