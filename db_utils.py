import datetime
import random

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import *


def connect_to_database(DSN):
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)

    return Session()


def get_publisher(session, publisher_input):
    if publisher_input.isdigit():
        publisher = session.query(Publisher).filter_by(id=int(publisher_input)).first()
    else:
        publisher = session.query(Publisher).filter_by(name=publisher_input).first()
    if publisher:
        return publisher
    else:
        print("Издатель не найден")
        return None


def get_sales_info(session, obj_publisher):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale). \
        join(Stock, Stock.book_id == Book.id). \
        join(Shop, Shop.id == Stock.shop_id). \
        join(Sale, Sale.stock_id == Stock.id). \
        filter(Book.publisher_id == obj_publisher.id)

    results = query.all()

    for result in results:
        print(f"{result[0]} | {result[1]} | {result[2]} | {result[3].strftime('%d-%m-%Y')}")


def fill_database(session, n):
    publishers = [Publisher(name=f'Publisher_{i}') for i in range(n)]
    shops = [Shop(name=f'Shop_{i}') for i in range(n)]
    books = []

    for i in range(n):
        publisher = random.choice(publishers)
        book = Book(title=f'Book_{i}', publisher=publisher)
        books.append(book)

    stocks = [
        Stock(
            book=random.choice(books),
            shop=random.choice(shops),
            count=random.randint(0, 100)
        ) for _ in range(n)
    ]
    sales = [
        Sale(
            price=random.randint(100, 1000),
            date_sale=datetime.datetime.now(),
            count=random.randint(1, 10),
            stock=random.choice(stocks)
        ) for _ in range(n)
    ]

    session.add_all(publishers)
    session.add_all(shops)
    session.add_all(books)
    session.add_all(stocks)
    session.add_all(sales)

    session.commit()
