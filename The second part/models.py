from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)
