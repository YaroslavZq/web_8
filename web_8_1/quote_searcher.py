def quote_searcher(quotes, command, searching_word):
	searching_quotes = []

	print(f'Search by {command}: {searching_word}')
	if command in ["tags", "tag"]:
		command = "tags"
		if len(searching_word) < 3:
			for quote in quotes(tags__istartswith=searching_word):
				searching_quotes.append({searching_word: quote['quote']})
		else:
			searching_word = searching_word.split(",")
			for quote in quotes:
				for tag in quote[command]:
					if tag in searching_word:
						searching_quotes.append({tag: quote['quote']})
	elif command == "exit":
		exit()
	else:
		if len(searching_word) < 3:
			for quote in quotes(author__istartswith=searching_word):
				searching_quotes.append({searching_word: quote['quote']})
		else:
			for quote in quotes:
				if searching_word == quote[command].replace(" ", ""):
					searching_quotes.append(quote['quote'])
	return searching_quotes

