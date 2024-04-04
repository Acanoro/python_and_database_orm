import os
from dotenv import load_dotenv

from db_utils import *

load_dotenv()


def main():
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    name = os.getenv("NAME")
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    DSN = f"postgresql://{user}:{password}@{host}:{port}/{name}"

    try:
        session, engine = connect_to_database(DSN)

        # создание таблиц
        # create_tables(engine)

        # создание объектов
        # fill_database(session=session, n=100)

        publisher_input = input()

        obj_publisher = get_publisher(session=session, publisher_input=publisher_input)

        get_sales_info(session=session, publisher_id_or_name=publisher_input)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    main()
