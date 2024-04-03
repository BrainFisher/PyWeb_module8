from mongoengine import *

# Підключення до бази даних MongoDB Atlas
connect('authors_quotes', host='your_mongodb_uri')

# Модель для зберігання даних про авторів
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

# Модель для зберігання цитат з посиланням на автора
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

import json

# Завантаження даних з файлів JSON
with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)

with open('quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)

# Збереження даних про авторів у базу даних
for author_data in authors_data:
    author = Author(
        fullname=author_data['fullname'],
        born_date=author_data['born_date'],
        born_location=author_data['born_location'],
        description=author_data['description']
    )
    author.save()

# Збереження цитат у базу даних, з посиланням на автора
for quote_data in quotes_data:
    author = Author.objects.get(fullname=quote_data['author'])
    quote = Quote(
        tags=quote_data['tags'],
        author=author,
        quote=quote_data['quote']
    )
    quote.save()

# Функція для пошуку цитат за різними параметрами
def search_quotes(query):
    command, value = query.split(':', 1)
    
    if command == 'name':
        author = Author.objects.get(fullname=value)
        quotes = Quote.objects(author=author)
    elif command == 'tag':
        quotes = Quote.objects(tags=value)
    elif command == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
    else:
        print('Невірна команда. Будь ласка, спробуйте ще раз.')
        return
    
    # Виведення результатів пошуку у форматі UTF-8
    for quote in quotes:
        print(f'Автор: {quote.author.fullname}')
        print(f'Цитата: {quote.quote}')
        print('Теги:', ', '.join(quote.tags))
        print()

# Основний цикл програми для пошуку цитат
while True:
    query = input('Введіть команду: ')
    if query == 'exit':
        break
    search_quotes(query)
