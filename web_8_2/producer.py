from datetime import datetime
import json
from random import randint

import pika
from faker import Faker
from contact_model import Contact

fake = Faker('uk_UA')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='sms_mock', exchange_type='direct')
channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_bind(exchange='sms_mock', queue='sms_queue')

channel.exchange_declare(exchange='email_mock', exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='email_mock', queue='email_queue')

def main():
	for i in range(10):
		Contact(fullname=fake.name(), email=fake.email(), number=fake.phone_number(), priority=randint(0, 1)).save()

	contacts = Contact.objects()
	count = 0
	for contact in contacts:
		if contact.priority == 0:
			count += 1
			message = {
				"message_number": count,
				'header': f'To: {contact.number}',
				'greetings': f'Hello: {contact.fullname}, your account created.',
				'id': str(contact.id),
				'created_at': datetime.now().isoformat()
			}

			channel.basic_publish(
				exchange='sms_mock',
				routing_key='sms_queue',
				body=json.dumps(message).encode(),
				properties=pika.BasicProperties(
					delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
				))
			print(" [x] Sent %r" % message)
		else:
			count += 1
			message = {
				"message_number": count,
				'header': f'To: {contact.email}',
				'greetings': f'Hello: {contact.fullname}, your account created.',
				'id': str(contact.id),
				'created_at': datetime.now().isoformat()
			}

			channel.basic_publish(
				exchange='email_mock',
				routing_key='email_queue',
				body=json.dumps(message).encode(),
				properties=pika.BasicProperties(
					delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
				))
			print(" [x] Sent %r" % message)
	connection.close()


if __name__ == '__main__':
	main()
