from mongoengine_models import Quote
import redis
from quote_searcher import quote_searcher

client = redis.StrictRedis(host='localhost', port=6379, password=None)

if __name__ == "__main__":
	quotes = Quote.objects()
	command, searching_word = input("What we are searching? (author/ tags): ").replace(" ", "").split(":")
	try:
		print(client.get(searching_word).decode())
	except Exception as e:
		results = quote_searcher(quotes, command, searching_word)
		for result in results:
			for key, value in result.items():
				print(key, ":", value)
				client.set(key, value)

