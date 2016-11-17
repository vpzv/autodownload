# Instruction (Ubuntu)
## Brief intro
With this script, My Raspberry PI3 checks new episodes from Zimuzu(login), and start download with Transmission. 
Once the downloads complete, you will get email alert.

## Prepare
1. To save power, low power devices are recommended, like Raspberry PI.
1. Install Python3
1. Register account on www.zimuzu.tv
1. Install Transmission on your LAN device(or SSH reverse connected ones in other LAN), which can be accessed through web(like 192.168.1.2:9091)

## Install
#### Install BeautifulSoup
```bash
pip3 install --upgrade pip
pip3 install beautifulsoup4
```
#### Install code
Download and extract the code(like in `/root/autodownloadjob`)
```bash
chmod u+x *.py
```

### Configure
Edit [constants.py](constants.py) accordingly

### Add your TV show
```sql
-- like in reset-db.sql
INSERT INTO tv(id, name, url, start_season, start_episode, site) VALUES(NULL,'Z Nation', 'http://www.zimuzu.tv/gresource/list/32725', 3, 7, 'ZiMuZu');
```


#### Add Cron schedule for Linux, execute `crontab -e` (Windows should add schedule task)
```
*/20 8-23 * * * /root/autodownloadjob/schedule.download.py
*/20 18-23 * * 1-5 /root/autodownloadjob/schedule.mail.py
*/20 12-13 * * 1-5 /root/autodownloadjob/schedule.mail.py
*/20 8-23 * * 6-7 /root/autodownloadjob/schedule.mail.py
```

## Common tools
#### Restore database
```bash
sqlite3 /var/www/db/tv.db < reset-db.sql
```
#### Clear database
```bash
rm /var/www/db/tv.db
```
