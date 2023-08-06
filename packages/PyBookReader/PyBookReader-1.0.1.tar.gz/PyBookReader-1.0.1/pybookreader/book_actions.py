import os
import datetime
from collections import namedtuple
import click
from tabulate import tabulate
import pdftotext
import keyboard

from .utils import truncate_long_text
from .models.book import Book


class BookAction:
    def __init__(
        self, books_dir=None, session=None, speak_engine=None, start_page=0, **kwargs
    ):
        self.books_dir = books_dir
        self.books = []
        self.session = session
        self.speak_engine = speak_engine
        self.current_page = 0
        self.start_page = start_page
        self.from_beginning = kwargs.get("from_beginning", False)

    def bookTup(self):
        return namedtuple("Book", ["num", "book_name", "book_path"])

    @staticmethod
    def warning(text):
        """ Show warning text message using `click.secho` with styling """
        fg = "yellow"
        bold = True
        click.echo()
        click.secho(text, fg=fg, bold=bold)

    def books_to_print(self):
        books = []
        headers = ["", "Book name", "Location"]
        for book in self.books:
            books.append(
                [
                    book.num,
                    truncate_long_text(book.book_name),
                    truncate_long_text(book.book_path),
                ]
            )
        return books, headers

    def books_from_db(self):
        books = self.session.query(Book).all()
        headers = ["ID", "Book name", "Location"]
        books_to_print = []
        for book in books:
            books_to_print.append(
                [
                    book.id,
                    truncate_long_text(book.name),
                    truncate_long_text(book.book_path),
                ]
            )
        return books_to_print, headers

    def print_books(self, saved=False):
        if saved:
            books, headers = self.books_from_db()
        else:
            books, headers = self.books_to_print()
        click.echo(tabulate(books, headers, tablefmt="grid"))

    def books_scanner(self, echo=True, saved=False):
        """
        Scan all the books available in the given directory.
        The books are not going to be stored in the database yet.
        """

        num = 0
        BookTup = self.bookTup()

        for bk in os.listdir(self.books_dir):
            book_name = bk.split(".pdf")[0]
            num += 1
            book_path = os.path.join(self.books_dir, bk)
            if os.path.isfile(book_path):
                book = BookTup(num, book_name, book_path)
                self.books.append(book)
        if echo:
            self.print_books(saved=saved)

    def store_books(self):
        """
        Scan and store the books in the given directory to the database
        """
        books_to_store = []
        self.books_scanner(echo=False)
        book_query = self.session.query(Book)
        for book in self.books:
            if not book_query.filter_by(name=book.book_name).count():
                books_to_store.append(
                    Book(name=book.book_name, book_path=book.book_path)
                )
        if books_to_store:
            self.session.add_all(books_to_store)
            self.session.commit()
            click.echo("Stored {} books to database".format(len(books_to_store)))
            return

        click.echo("No books to store")

    def read_book(self, book):
        if not self.speak_engine:
            raise Exception("pyttsx3 is not initialized")

        with open(book.book_path, "rb") as book_file:
            # convert deque to list
            # TODO: use deque but have to make it slicable
            pages = list(pdftotext.PDF(book_file))

        current_page = book.stop_at_page
        if not self.from_beginning:
            if self.start_page:
                pages = pages[self.start_page :]
                self.current_page = self.start_page
            elif current_page and not self.start_page:
                pages = pages[current_page:]
                self.current_page = current_page

        click.clear()
        click.echo()
        try:
            for ind, page in enumerate(pages):
                if self.from_beginning or (not self.start_page and not current_page):
                    self.current_page = ind

                click.echo(page)
                click.echo()
                click.secho("Press Ctrl + C to stop reading", bold=True)

                self.speak_engine.say(page)
                self.speak_engine.runAndWait()
                click.clear()

                # TODO: Make it possible to skip the current page and jump to the next page when press a key.
                # Maybe try asyncio?
                # Already added `keyboard` library for this.
        except KeyboardInterrupt:
            click.echo()
            click.echo("Stoped at page {}".format(self.current_page))

            click.echo("Do you want to save the current progess? [y/n] ", nl=False)
            answer = click.getchar()
            click.echo()
            if answer in ["y", "Y", "yes"]:
                book.stop_at_page = self.current_page
                book.last_read = datetime.datetime.utcnow()
                self.session.add(book)
                self.session.commit()
                click.echo("Your progess is saved.")
            else:
                click.echo("Abort!")
