from mongoengine import connect, Document, StringField, BooleanField, IntField

connect(host='')


class Contact(Document):
	fullname = StringField(required=True)
	email = StringField(required=True, unique=True)
	number = StringField(unique=True)
	priority = IntField()
	status_message = BooleanField(default=False)
