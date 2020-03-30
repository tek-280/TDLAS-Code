#import coloredlogs
#import logging
import requests
import json
#import redis
import sys

#relay = config.get("relay")

print('hello Thomas')

#temp_text='curl -X PUT -d '{"Action":"TCP","Host":"192.168.98.137","Port":5300,"Value":"*read?\n"}' '
data={"Action":"TCP","Host":"192.168.98.137","Port":5300,"Value":"*read?\r"}

req = requests.post("http://i75464.berlin.ptb.de:55555", data=json.dumps(data))
res = req.json()
print(res)
