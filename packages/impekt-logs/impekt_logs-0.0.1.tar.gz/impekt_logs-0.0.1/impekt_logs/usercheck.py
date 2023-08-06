appid = "3333"
appkey = "5555"


name = "ebru"
mail = "ebru.navruz@impektra.com"


import users
import json
import time
import Producer

dict = users.dictionary
value = dict.get(appid)

if value is None:
	print("Hatalı kullanıcı id'si")
data =0


def check(value,appid,appkey,name,mail):
	if value == appkey:
		print("Doğru kullanıcı")
		
		try:
			jsonn = {"appid":appid,"appkey":appkey,"name": name,"mail" : mail,"data":str(data)}

		except:
			jsonn = {"appid":appid,"appkey":appkey,"name": "not given","mail" : "not given","data":"xxx"}

		Producer.send_values(json.dumps(jsonn))
		time.sleep(2)

	else :
		print("hatalı kullanıcı key'i")

check(value,appid,appkey,name,mail)
