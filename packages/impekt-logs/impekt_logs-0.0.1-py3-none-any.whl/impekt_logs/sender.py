## Kullanıcının bilgilerini çekmek ?
import usercheck
from confluent_kafka import Consumer,KafkaError
import json

topic = "log"

consumer = Consumer({
	'bootstrap.servers': "pkc-ep9mm.us-east-2.aws.confluent.cloud:9092",
	'sasl.mechanisms': 'PLAIN',
	'security.protocol': 'SASL_SSL',
	'sasl.username': 'IWML43SVQPFVE75N',
	'sasl.password': 'AJgJMi8bXJP4kNhObVKk2pwt43paUhfllAGRboEDQSlV2av6qHEHTiBifDbMP6T0',
	'group.id': 'group3',
	'enable.auto.commit': 'True',
	'auto.offset.reset': 'earliest',
	'default.topic.config': {'auto.offset.reset': 'smallest'},

})

consumer.subscribe([topic])

id_ = usercheck.appid
key_ = usercheck.appkey


datalog = []

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
    		print(msg)
    		print(len(msg))
    		msg = json.loads((msg.value().decode("utf-8")))

    		if msg['appid']==id_ and msg['appkey']==key_:
    			datalog.append(msg)
    		print(datalog)

except KeyboardInterrupt:
    pass
finally:
	consumer.close()

