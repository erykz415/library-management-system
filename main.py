from controllers.auth_service import AuthService
from controllers.library_proxy import LibraryProxy
from controllers.library_service import LibraryService
from models.library_database import LibraryDatabase
from controllers.book import Book

auth = AuthService()
service = LibraryProxy(LibraryService())
library = LibraryDatabase()

print("register")
auth.register(
    "librarian", "Elizabeth", "Taylor", "e_taylor", "etaylor@mail.com", "pass123"
)
auth.register("student", "James", "Smith", "j_smith", "jsmith@mail.com", "pass456")
auth.register("lecturer", "David", "Walker", "d_walker", "dwalker@mail.com", "pass789")

print("\nlogin")
librarian = auth.login("e_taylor", "pass123")
student = auth.login("j_smith", "pass456")
lecturer = auth.login("d_walker", "pass789")

print("\npermissions")
print(f"librarian: {librarian.get_permissions()}")
print(f"student: {student.get_permissions()}")
print(f"lecturer: {lecturer.get_permissions()}")

print("\nimport books")
service.import_book_from_external_db("9780744586381", librarian)
service.import_book_from_external_db("9780399256653", librarian)

book = Book(
    title="The Associate",
    author="John Grisham",
    isbn="9780739328231",
    genre="Thriller",
    published_year=2009,
)
service.add_book(book, librarian)

service.update_book("9780739328231", librarian, published_year=2010)

print(f"There are {len(library.list_books())} books")

service.remove_book("9780739328231", librarian)
print(f"There are {len(library.list_books())} books")

print("\nobserve books")
service.borrow_book("9780744586381", lecturer)
service.observe_book("9780744586381", student)
service.return_book("9780744586381", lecturer)

print("\nborrow and return")
service.borrow_book("9780744586381", lecturer)
service.return_book("9780744586381", lecturer)
service.borrow_book("9780744586381", student)
service.return_book("9780744586381", student)

print("\nhistory")
service.show_history(student)

print("\nhistory all")
for cmd in service.get_history():
    print(cmd.describe())


# for book in library.list_books():
#     print(book)
