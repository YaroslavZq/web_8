from mongoengine import connect, Document, StringField, ReferenceField, ListField
import json

connect(host='')


class Author(Document):
	fullname = StringField(required=True, unique=True)
	born_date = StringField(max_length=50)
	born_location = StringField(max_length=50)
	description = StringField()


class Quote(Document):
	quote = StringField(required=True, max_length=500, min_length=5)
	author = StringField()
	author_id = ReferenceField(Author)
	tags = ListField(StringField())


def download_author(file):
	author = json.load(file)
	Author().from_json(json.dumps(author)).save()


def download_authors_many(file):
	authors = json.load(file)
	for author in authors:
		Author().from_json(json.dumps(author)).save()


def download_quote(file):
	quote = json.load(file)
	Quote().from_json(json.dumps(quote)).save()


def download_quotes_many(file):
	quotes = json.load(file)
	for quote in quotes:
		Quote().from_json(json.dumps(quote)).save()


def update_quotes():
	quotes = Quote.objects()
	authors = Author.objects()
	for quote in quotes:
		name = quote.author
		for author in authors:
			if author.fullname == name:
				id_ = author.id
				quote.update(author_id=id_)


def searcher():
	command = input("What we are searching? (name/ tag/ tags): ")
	searching_word = input('Please enter searching word(s): ')
	print(f'Search by {command}: {searching_word}')


