from datetime import datetime, timedelta
from .models import Book, Member, Loan
from .storage import Storage
from .utils import generate_id

def add_book(data_dir: str, isbn: str, title: str, author: str, copies: int) -> Book:
    books = Storage.read_csv(f"{data_dir}/books.csv", Book)
    
    if any(b.ISBN == isbn for b in books):
        raise ValueError("Book with this ISBN already exists")
        
    book = Book(ISBN=isbn, Title=title, Author=author, CopiesAvailable=copies)
    books.append(book)
    Storage.write_csv(f"{data_dir}/books.csv", books)
    return book

def remove_book(data_dir: str, isbn: str):
    books = Storage.read_csv(f"{data_dir}/books.csv", Book)
    books = [b for b in books if b.ISBN != isbn]
    Storage.write_csv(f"{data_dir}/books.csv", books)

def issue_book(data_dir: str, isbn: str, member_id: str) -> Loan:
    # Get book and check availability
    books = Storage.read_csv(f"{data_dir}/books.csv", Book)
    book = next((b for b in books if b.ISBN == isbn), None)
    
    if not book:
        raise ValueError("Book not found")
    if book.CopiesAvailable <= 0:
        raise ValueError("No copies available")
    
    # Update book copies
    book.CopiesAvailable -= 1
    Storage.write_csv(f"{data_dir}/books.csv", books)
    
    # Create loan record
    loans = Storage.read_csv(f"{data_dir}/loans.csv", Loan)
    today = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    loan = Loan(
        LoanID=generate_id(),
        ISBN=isbn,
        MemberID=member_id,
        IssueDate=today,
        DueDate=due_date
    )
    
    loans.append(loan)
    Storage.write_csv(f"{data_dir}/loans.csv", loans)
    return loan

def return_book(data_dir: str, loan_id: str):
    # Update loan record
    loans = Storage.read_csv(f"{data_dir}/loans.csv", Loan)
    loan = next((l for l in loans if l.LoanID == loan_id), None)
    
    if not loan:
        raise ValueError("Loan not found")
    
    loan.ReturnDate = datetime.now().strftime("%Y-%m-%d")
    Storage.write_csv(f"{data_dir}/loans.csv", loans)
    
    # Update book copies
    books = Storage.read_csv(f"{data_dir}/books.csv", Book)
    book = next((b for b in books if b.ISBN == loan.ISBN), None)
    if book:
        book.CopiesAvailable += 1
        Storage.write_csv(f"{data_dir}/books.csv", books)

def get_overdue_loans(data_dir: str):
    loans = Storage.read_csv(f"{data_dir}/loans.csv", Loan)
    today = datetime.now().strftime("%Y-%m-%d")
    
    return [
        loan for loan in loans 
        if not loan.ReturnDate and loan.DueDate < today
    ]