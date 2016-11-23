#!/usr/bin/python3
import sys, os, re
import dao, constants, zimuzu, boxdownload
from requests import Request, Session

sys.stdout = open("/root/autodownloadjob/schedule.download.log", encoding='utf-8', mode='w')
sys.stderr = open("/root/autodownloadjob/schedule.download.error.log", encoding='utf-8', mode='w')

def download_for_zimuzu(tv):
	print('[%s] from S%sE%s' % (tv['name'], tv['start_season'], tv['start_episode']))
	series_list = zimuzu.fetch_all_series_for_zimuzu(tv)
	headers = boxdownload.find_box_http_header()
	if not series_list or not headers:
		return

	for series in series_list:
		groups = re.compile(r'\.S(\d{1,3}).*E(\d{1,3})\.').search(series['title'])
		if not groups:
			continue
		season = groups.group(1)
		episode = groups.group(2)
		if(int(tv['start_season']) > int(season) or int(tv['start_episode']) >= int(episode)):
			continue
		print(' - Add S%sE%s' % (season, episode))
		if boxdownload.send_download_link_to_box(headers, series['link']):
			dao.save_series(tv['id'], season, episode, series['link'], series['title'], constants.DOWLOADING_FLAG)
			dao.update_tv_series_progress(tv['id'], season, episode)


def main():
	if not os.path.isfile(constants.sqlite_file):
		dao.create_db()
	else:
		print('Using database: %s' % constants.sqlite_file)

	tv_list = dao.list_tv()
	if not tv_list:
		print('No TV found in db')
		return
	else:
		print('Checking %s TVs' % len(tv_list))

	for tv in tv_list:
		if tv and tv['url'] and 'zimuzu.tv' in tv['url']:
			download_for_zimuzu(tv)


main()
