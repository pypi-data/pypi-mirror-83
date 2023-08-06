from confluent_kafka import Consumer,KafkaError
import json

topic = "log"
import time
from pymongo import MongoClient
import pymongo	


consumer = Consumer({
	'bootstrap.servers': "pkc-ep9mm.us-east-2.aws.confluent.cloud:9092",
	'sasl.mechanisms': 'PLAIN',
	'security.protocol': 'SASL_SSL',
	'sasl.username': 'IWML43SVQPFVE75N',
	'sasl.password': 'AJgJMi8bXJP4kNhObVKk2pwt43paUhfllAGRboEDQSlV2av6qHEHTiBifDbMP6T0',
	'group.id': 'group1',
	'auto.offset.reset': 'earliest',
	'default.topic.config': {'auto.offset.reset': 'smallest'},
})

consumer.subscribe([topic])
# Process messages

connect = MongoClient()
print("Connected successfully!!!")

db = connect.mynewdb
collection = db.newCollection


try:
	while True:
	    msg = consumer.poll(1.0)

	    if msg is None:
	    	print("Message is None !")
	    	continue

	    if msg.error():
	        print("Consumer error: {}".format(msg.error()))
	        continue
	    else:
		    msg_json = msg.value().decode('utf-8')
		    msg_json = json.loads(msg_json)
		    collection.insert_one(msg_json)
		    cursor = collection.find()

		    for record in cursor:
	    			print(record)
	    
except KeyboardInterrupt:
    pass
finally:
	consumer.close()


