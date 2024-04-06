import pika
import json
import faker
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect('contacts_database')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672))

channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Функція для генерації фейкових контактів та їх збереження в базі даних


def generate_contacts(num_contacts):
    fake = faker.Faker()
    contacts = []
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()
        contacts.append(contact)
    return contacts

# Функція для надсилання ідентифікаторів контактів у чергу RabbitMQ


def send_to_queue(contacts):
    for contact in contacts:
        message = {'contact_id': str(contact.id)}
        channel.basic_publish(
            exchange='', routing_key='email_queue', body=json.dumps(message))
        print(f"Sent contact {contact.id} to the queue")


if __name__ == '__main__':
    num_contacts = 5  # Задаємо кількість фейкових контактів
    contacts = generate_contacts(num_contacts)
    send_to_queue(contacts)
