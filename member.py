from .models import Book, Loan
from .storage import Storage

def search_books(data_dir: str, query: str) -> list[Book]:
    books = Storage.read_csv(f"{data_dir}/books.csv", Book)
    query = query.lower()
    return [
        b for b in books 
        if query in b.Title.lower() or query in b.Author.lower()
    ]

def get_member_loans(data_dir: str, member_id: str) -> list[Loan]:
    loans = Storage.read_csv(f"{data_dir}/loans.csv", Loan)
    return [l for l in loans if l.MemberID == member_id]