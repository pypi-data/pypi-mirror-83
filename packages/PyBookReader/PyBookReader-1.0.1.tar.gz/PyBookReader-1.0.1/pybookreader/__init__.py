import click
import pyttsx3

from .book_actions import BookAction
from .models import base
from .models.book import Book
from .settings import Settings


@click.group()
@click.pass_context
def book_reader(ctx):
    ctx.ensure_object(dict)

    settings = Settings()
    ctx.obj["settings"] = settings
    ctx.obj["session"] = settings.Session()
    base.Base.metadata.create_all(settings.sql_engine)


@book_reader.command()
@click.option("-l", "--location", help="Path to the folder contains your books")
@click.option("--save", is_flag=True, help="Save the books after scanning them")
@click.pass_context
def scan_books(ctx, location, save):
    """Scan books in a given directory"""
    actions = BookAction(books_dir=location, session=ctx.obj["session"])
    if save:
        actions.store_books()
    actions.books_scanner(saved=save)


@book_reader.command()
@click.pass_context
def show_all_books(ctx):
    """Show all available books stored in the database"""
    actions = BookAction(session=ctx.obj["session"])
    click.echo("Available books in the database")
    actions.print_books(saved=True)


@book_reader.command()
@click.option("-b", "--book", help="Name of the book you want to read", default=None)
@click.option("-i", "--id", help="ID of the book if it is in the database", default=0)
@click.option(
    "--start-from-page", help="Start reading from the specified page", default=0
)
@click.option(
    "--start-from-beginning",
    help="Start reading all over from the begining",
    is_flag=True,
)
@click.pass_context
def read_book_from_db(ctx, book, id, start_from_page, start_from_beginning):
    """
    Read a book already stored in the database by the book's name
    or its ID.
    """
    engine = pyttsx3.init()
    actions = BookAction(
        session=ctx.obj["session"],
        speak_engine=engine,
        start_page=start_from_page,
        from_beginning=start_from_beginning,
    )
    book_query = actions.session.query(Book)
    book_to_read = None
    if book:
        book_to_read = book_query.filter_by(name=book).first()
        if not book_to_read:
            actions.warning(
                "This book with the name '{}' does not exist in the database.".format(
                    book
                )
            )
            return

    if id:
        book_to_read = book_query.get(int(id))
        if not book_to_read:
            actions.warning(
                "This book with the ID of '{}' does not exist or might be deleted already. Check the ID again or try using the book's name".format(
                    id
                )
            )
            return

    if not book_to_read:
        actions.warning(
            "Please specify the book you want to ready by its name or ID in the database"
        )
        return

    actions.read_book(book_to_read)
