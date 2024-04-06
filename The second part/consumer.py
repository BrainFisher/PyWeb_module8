import pika
import json
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect('contacts_database')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672))

channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Функція-заглушка для надсилання email


def send_email(email, message):
    print(f"Sending email to {email}: {message}")

# Функція для обробки повідомлень з черги RabbitMQ


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects.get(id=contact_id)
    if not contact.sent:
        send_email(contact.email, "Test message")
        contact.sent = True
        contact.save()
        print(f"Email sent to {contact.email}")
    else:
        print(f"Email already sent to {contact.email}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Підписка на чергу та очікування повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
