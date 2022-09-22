from mysql.connector import connect, Error


class DataBase:
    """Class used to help work with db"""
    def __init__(self, host: str, user: str, password: str):
        """
        :param host: host's ip
        :param user: username to log in to database
        :param password: password to log in to database
        """
        self.__host = host
        self.__user = user
        self.__password = password
        self.connection = None

    def __connect(self):
        """
        Try to connect to certain db in the given server
        :return: None
        """
        try:
            self.connection = connect(host=self.__host, user=self.__user, password=self.__password,
                                      database="cf19571_booksdb")
        except Error as e:
            print(f"Error: {e}")

    def save_book(self, name: str):
        """
        Save book name in db
        :param name: book name
        :return: None
        """
        self.__connect()
        insert_book = f'INSERT INTO books (book_name) VALUES("{name}")'
        self.connection.cursor().execute(insert_book)
        self.connection.commit()
        self.connection.disconnect()

    def delete_book(self, name: str):
        """
        Delete book from db by name
        :param name: book name
        :return: None
        """
        self.__connect()
        delete_book = f'DELETE FROM books WHERE book_name = "{name}"'
        self.connection.cursor().execute(delete_book)
        self.connection.commit()
        self.connection.disconnect()

    def show_books(self):
        """
        :return: list of saved books
        """
        print(self.connection, 1)
        self.__connect()
        print(self.connection, 2)
        show_books = f'SELECT book_name FROM books'
        with self.connection.cursor() as cursor:
            cursor.execute(show_books)
            res = [book[0] for book in cursor.fetchall()]
        self.connection.disconnect()
        return res
