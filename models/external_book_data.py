from typing import Dict

BOOK_DB: Dict[str, dict] = {
    "9780744586381": {
        "title": "The reluctant dragon",
        "author": "Kenneth Grahame, Jim Weiss, Ernest H. Shepard, Michael Hague",
        "description": "All the Reluctant Dragon wants to do is laze by his cave and make up poetry! "
        "He certainly doesn't want to fight, but it seems he will have no choice when St. George arrives. "
        "Fortunately the dragon has one friend - the shepherd's son, a small boy with a great deal of sense "
        "and imagination ",
        "genre": "Children's Fantasy",
        "published_year": 1898,
    },
    "9780399256653": {
        "title": "The Insomniacs",
        "author": "Allison Winn Scotch",
        "description": "In the city that never sleeps, it’s not always easy to share what’s on your mind with "
        "the people who know you best. Huddled in an all-night diner over coffee and pancakes, "
        "a lonely middle-aged mom, an injured baseball pro, an elusive retiree, and a young waitress "
        "examine the thoughts that plague them in the middle of the night.",
        "genre": "Mystery, Thriller",
        "published_year": 2026,
    },
}


class BookService:
    def __init__(self):
        self.book_db: Dict[str, dict] = BOOK_DB

    def get_book_by_isbn(self, isbn: str) -> dict | None:
        return self.book_db.get(isbn)
