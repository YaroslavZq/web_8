from mongoengine_models import download_authors_many, download_quotes_many, update_quotes


if __name__ == "__main__":
	with open("authors.json") as file:
		download_authors_many(file)
	with open("quotes.json") as file:
		download_quotes_many(file)
	update_quotes()
