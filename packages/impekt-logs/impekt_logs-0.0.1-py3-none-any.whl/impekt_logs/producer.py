from confluent_kafka import Producer, KafkaError
import time
import json

topic = "log" #log


producer = Producer({
	'bootstrap.servers': "pkc-ep9mm.us-east-2.aws.confluent.cloud:9092",
	'sasl.mechanisms': 'PLAIN',
	'security.protocol': 'SASL_SSL',
	'sasl.username': 'IWML43SVQPFVE75N',
	'sasl.password': 'AJgJMi8bXJP4kNhObVKk2pwt43paUhfllAGRboEDQSlV2av6qHEHTiBifDbMP6T0',
})


def packed(err, msg):

	if err is not None:
		print("Failed to deliver message: {}".format(err))
	else:
	   
		print("Produced record to topic {} partition [{}] @ offset {}"
			  .format(msg.topic(), msg.partition(), msg.offset()))


def send_values(value):
	record_value = str(value)
	producer.produce(topic, (record_value).encode('utf-8'), on_delivery=packed)
	producer.poll(1.0)
	producer.flush()
	
