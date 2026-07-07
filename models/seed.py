from controllers.auth_service import AuthService
from models.library_database import LibraryDatabase
from controllers.book import Book


def seed_users(auth: AuthService) -> None:
    users = [
        {
            "role": "student",
            "first_name": "James",
            "last_name": "Smith",
            "username": "j_smith",
            "email": "jsmith@mail.com",
            "password": "pass1234",
        },
        {
            "role": "lecturer",
            "first_name": "David",
            "last_name": "Walker",
            "username": "d_walker",
            "email": "dwalker@mail.com",
            "password": "456pass",
        },
        {
            "role": "librarian",
            "first_name": "Elizabeth",
            "last_name": "Taylor",
            "username": "e_taylor",
            "email": "etaylor@mail.com",
            "password": "pass987",
        },
    ]
    for user in users:
        auth.register(**user)


def seed_books() -> None:
    books = [
        Book(
            title="Pride and Prejudice",
            author="Jane Austen, Anna Quindlen",
            isbn="9780141439518",
            description="Pride and Prejudice is the second published novel (but third to be written) by English author Jane Austen, "
            "written when she was aged 20–21, and later published in 1813.A novel of manners, it follows the character "
            "development of Elizabeth Bennet, the protagonist of the book, who learns about the repercussions of hasty judgments "
            "and comes to appreciate the difference between superficial goodness and actual goodness.",
            genre="Classic Regency novel",
            published_year=1813,
        ),
        Book(
            title="1984",
            author="George Orwell, Thomas Pynchon",
            isbn="9780452284234",
            description="Nineteen Eighty-Four (also published as 1984) is a dystopian speculative "
            "fiction novel by the English writer George Orwell. It was published on 8 June 1949 "
            "by Secker & Warburg as Orwell's ninth and final completed book. Thematically, "
            "it centres on totalitarianism, mass surveillance and repressive regimentation "
            "of people and behaviours.[3][4] Nineteen Eighty-Four has been often regarded as a classic "
            "and has been acknowledged for its impact on twentieth-century literature.",
            genre="Dystopian",
            published_year=1949,
        ),
        Book(
            title="Lord of the Flies",
            author="William Golding",
            isbn="9780140283334",
            description="Lord of the Flies is the 1954 debut novel of British author William Golding. "
            "The plot concerns a group of prepubescent British boys who are stranded "
            "on an uninhabited island and their disastrous attempts to govern themselves "
            "that lead to a descent into savagery. The novel's themes include morality, "
            "leadership, and the tension between civility and chaos.",
            genre="Allegorical novel",
            published_year=1954,
        ),
        Book(
            title="Time will tell",
            author="Lauralee Bliss",
            isbn="1593102593",
            description="Everyone loves a bargain - but Connie Ortiz gets more than she bargained for when "
            "she buys an old cuckoo clock at a yard sale. Suddenly, strange people begin entering her life. "
            "An elderly man appears at her doorstep, offering to buy the clock. "
            "The older lady in charge of the sale urges Connie to keep the clock at all cost. And her handsome "
            "boss arrives on the scene to play referee. Truth be told, Lance Adams cares less about refereeing "
            "than he does getting to know Connie. He finds her quite intriguing - but so, too, is her fascination with "
            "a clock that everyone seems to want. What is it about this clock that has people in a frenzy? Can love resolve this mystery? "
            "Only time will tell.",
            genre="Christian Fiction",
            published_year=2011,
        ),
    ]

    db = LibraryDatabase()

    for book in books:
        db.add_book(book)
