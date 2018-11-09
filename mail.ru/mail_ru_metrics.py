#!/usr/local/bin/python3
import sys
import json
import requests
import datetime
# check for config present 
if len(sys.argv)==1:
    print("Need config as argument!")
    exit(1)
try:
    config_file = open(sys.argv[1], 'r')
    config = json.loads(config_file.read())
    config_file.close()
except Exception:
    print("Error reding config file!")
    exit(2)
# get mail.ru access token
params = (
    ('client_id','postmaster_api_client'),
    ('grant_type','refresh_token'),
    ('refresh_token',config["refresh_token"]),
)
answer = json.loads(requests.post('https://o2.mail.ru/token', params=params).text)
# get mail.ru metrics for domain
header = {
    'Bearer': answer["access_token"],
}
params = (
    ('domain',config["domain"]),
    ('date_from','{0:%Y-%m-%d}'.format(datetime.datetime.now())),
    ('date_to','{0:%Y-%m-%d}'.format(datetime.datetime.now())),
)
result = json.loads(requests.get('https://postmaster.mail.ru/ext-api/stat-list/', headers=header, params=params).text)
# printing output with InfluxDB format
print('mail_ru,domain='+result["data"][0]["domain"]+' sent='+str(result["data"][0]["messages_sent"])+',spam='+str(result["data"][0]["spam"])+',probably_spam='+str(result["data"][0]["probably_spam"]))
