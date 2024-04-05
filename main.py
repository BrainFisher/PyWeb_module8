from mongoengine import connect, Document, StringField, DateTimeField, ListField, ReferenceField
from datetime import datetime
import json

# Підключення до MongoDB Atlas
connect('my_database',
        host='mongodb+srv://brainfisher13:<"PASS">@cluster0.3ufzbcf.mongodb.net/')

# Модель для авторів


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

# Модель для цитат


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

# Функція для завантаження даних з JSON файлів у базу даних


def load_data():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            Author(**author_data).save()

    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                quote_data['author'] = author
                Quote(**quote_data).save()

# Функція для пошуку цитат за тегом, ім'ям автора або набором тегів


def search_quotes(query):
    if query.startswith('name:'):
        author_name = query.split(':')[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
    elif query.startswith('tag:'):
        tag = query.split(':')[1].strip()
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print(quote.quote)
    elif query.startswith('tags:'):
        tags = query.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(quote.quote)

# Головна функція для виконання скрипту


def main():
    load_data()
    while True:
        query = input("Введіть команду: ")
        if query == 'exit':
            break
        search_quotes(query)


if __name__ == "__main__":
    main()
