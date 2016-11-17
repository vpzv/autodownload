#!/usr/bin/python3
import sys, os, json, codecs, time, sqlite3, re
import constants

def create_db():
	print('Creating database...')
	conn = sqlite3.connect(constants.sqlite_file)
	conn.execute('''
	  CREATE TABLE tv
	  (ID       INTEGER PRIMARY KEY,
	  name      TEXT    NOT NULL,
	  url    	TEXT,
	  site    	TEXT NOT NULL,
	  start_season	INTEGER default 1,
	  start_episode	INTEGER default 1,
	  time      TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
	conn.execute('''
	  CREATE TABLE series
	  (ID       INTEGER PRIMARY KEY,
	  TV_ID     INTEGER,
	  season 	INTEGER,
	  episode 	INTEGER,
	  title 	TEXT,
	  link 		TEXT,
	  status	TEXT default 'Downloaded',
	  time      TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')    
	
	print(' Generating default data...')
	cur = conn.cursor()
	cur.execute("INSERT INTO tv(id, name, url, start_season, start_episode, site) VALUES(NULL, ?, ?, ?,?,?)", 
		('Westworld 2016', 'http://www.zimuzu.tv/gresource/list/33701', 1, 4 , constants.ZIMUZU_NAME))
	conn.commit()
	conn.close()
	print(' Done.')


def update_tv_series_progress(tv_id, season, episode):
	conn = sqlite3.connect(constants.sqlite_file)
	cur = conn.cursor()
	cur.execute("update tv set start_season=?, start_episode=? where tv.id=? and start_season <= ? and start_episode < ?", 
		(season, episode, tv_id, season, episode))
	conn.commit()
	conn.close()


def list_tv():
	conn = sqlite3.connect(constants.sqlite_file)
	cur = conn.cursor()
	cur.execute("SELECT id, name, url, start_season, start_episode, site FROM tv ORDER BY name ASC")
	result = cur.fetchall()
	tvs = []
	for row in result:
		tvs.append({'id': row[0], 'name': row[1], 'url':row[2], 'start_season':row[3], 'start_episode':row[4], 'site':row[5]})
	conn.close()
	return tvs


def save_series(tv_id, season, episode, link, title, status):
	conn = sqlite3.connect(constants.sqlite_file)
	cur = conn.cursor()
	cur.execute("INSERT INTO series(ID,TV_ID,season,episode,link,title,status) VALUES(NULL,?,?,?,?,?,?)", 
		(tv_id, season, episode, link, title, status))
	conn.commit()
	conn.close()


def find_series_inprogress():
	conn = sqlite3.connect(constants.sqlite_file)
	cur = conn.cursor()
	cur.execute("SELECT ID,TV_ID,season,episode,link,title,status FROM series where status=? ORDER BY time ASC", (constants.DOWLOADING_FLAG,))
	result = cur.fetchall()
	tvs = []
	for row in result:
		tvs.append({'id': row[0], 'TV_ID': row[1], 'season':row[2], 'episode':row[3], 'link':row[4], 'title':row[5], 'status':row[6]})
	conn.close()
	return tvs


def update_series_status(series_id, status):
	conn = sqlite3.connect(constants.sqlite_file)
	cur = conn.cursor()
	cur.execute("update series set status=? where ID=?", (status, series_id))
	conn.commit()
	conn.close()

#print(find_series_inprogress())
