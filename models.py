import sqlalchemy as sq
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True, nullable=False)

    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publishers.id"), nullable=False)
    publisher = relationship("Publisher", backref="publishers")


class Publisher(Base):
    __tablename__ = 'publishers'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Shop(Base):
    __tablename__ = 'shops'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Stock(Base):
    __tablename__ = 'stocks'

    id = sq.Column(sq.Integer, primary_key=True)

    book_id = sq.Column(sq.Integer, sq.ForeignKey("books.id"), nullable=False)
    book = relationship("Book", backref="books")

    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shops.id"), nullable=False)
    shop = relationship("Shop", backref="shops")

    count = sq.Column(sq.Integer, default=0)

    def __str__(self):
        return 'stock'


class Sale(Base):
    __tablename__ = 'sales'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, default=0)
    date_sale = sq.Column(DateTime, nullable=False)
    count = sq.Column(sq.Integer, default=0)

    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stocks.id"), nullable=False)
    stock = relationship("Stock", backref="stocks")

    def __str__(self):
        return 'sales'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
