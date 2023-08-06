from setuptools import setup, find_packages

with open("readme.md", "r") as read_me:
    long_description = read_me.read()

setup(
    name="PyBookReader",
    version="1.0.1",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dangquangdon/Python-Book-Reader-CLI",
    install_requires=[
        "click==7.1.2",
        "pyttsx3==2.90",
        "SQLAlchemy==1.3.20",
        "tabulate==0.8.7",
        "pdftotext==2.1.5",
        "alembic==1.4.3",
        "keyboard==0.13.5",
        "black",
        "wheel",
        "twine",
    ],
    entry_points="""
        [console_scripts]
        pybookreader=pybookreader:book_reader
    """,
)
