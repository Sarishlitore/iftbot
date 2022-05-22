from mysql.connector import connect, Error


class DataBase:

    def __init__(self, host: str, user: str, password: str):
        self.__host = host
        self.__user = user
        self.__password = password
        self.connection = None

    def __connect(self):
        try:
            self.connection = connect(host=self.__host, user=self.__user, password=self.__password, database="booksdb")
        except Error as e:
            print(e)

    def save_book(self, name: str):
        self.__connect()
        insert_book = f'INSERT INTO books (book_name) VALUES("{name}")'
        self.connection.cursor().execute(insert_book)
        self.connection.commit()
        self.connection.disconnect()

    def delete_book(self, name: str):
        self.__connect()
        delete_book = f'DELETE FROM books WHERE book_name = "{name}"'
        self.connection.cursor().execute(delete_book)
        self.connection.commit()
        self.connection.disconnect()

    def show_books(self):
        self.__connect()
        show_books = f'SELECT book_name FROM books'
        with self.connection.cursor() as cursor:
            cursor.execute(show_books)
            res = [book[0] for book in cursor.fetchall()]
        self.connection.disconnect()
        return res
