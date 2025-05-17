import argparse
from lib.auth import login, logout, register_member, get_current_user
from lib.librarian import *
from lib.member import *
from lib.utils import format_date
import os

def setup_argparse():
    parser = argparse.ArgumentParser(description="Library Management System")
    parser.add_argument("--data-dir", default="./data", help="Directory to store CSV files")
    return parser.parse_args()

def main():
    args = setup_argparse()
    os.makedirs(args.data_dir, exist_ok=True)
    
    while True:
        print("\n=== Library Management System ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("> ").strip()
        
        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            user = login(args.data_dir, email, password)
            
            if user:
                if user.Role == "librarian":
                    librarian_menu(args.data_dir)
                else:
                    member_menu(args.data_dir, user.MemberID)
            else:
                print("Invalid credentials")
                
        elif choice == "2":
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            register_member(args.data_dir, name, email, password)
            print("Registration successful!")
            
        elif choice == "3":
            break

def librarian_menu(data_dir: str):
    while True:
        print("\n=== Librarian Dashboard ===")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Overdue List")
        print("6. Logout")
        
        choice = input("> ").strip()
        
        try:
            if choice == "1":
                isbn = input("ISBN: ")
                title = input("Title: ")
                author = input("Author: ")
                copies = int(input("Copies: "))
                add_book(data_dir, isbn, title, author, copies)
                print("Book added successfully!")
                
            elif choice == "2":
                isbn = input("ISBN to remove: ")
                remove_book(data_dir, isbn)
                print("Book removed successfully!")
                
            elif choice == "3":
                isbn = input("ISBN to issue: ")
                member_id = input("Member ID: ")
                loan = issue_book(data_dir, isbn, member_id)
                print(f"✔ Book issued. Due on {format_date(loan.DueDate)}")
                
            elif choice == "4":
                loan_id = input("Loan ID to return: ")
                return_book(data_dir, loan_id)
                print("Book returned successfully!")
                
            elif choice == "5":
                overdue = get_overdue_loans(data_dir)
                if overdue:
                    print("\n=== Overdue Books ===")
                    for loan in overdue:
                        print(f"Loan ID: {loan.LoanID}, ISBN: {loan.ISBN}, Member: {loan.MemberID}, Due: {format_date(loan.DueDate)}")
                else:
                    print("No overdue books")
                    
            elif choice == "6":
                logout()
                break
                
        except Exception as e:
            print(f"Error: {str(e)}")

def member_menu(data_dir: str, member_id: str):
    while True:
        print("\n=== Member Dashboard ===")
        print("1. Search Books")
        print("2. My Loans")
        print("3. Logout")
        
        choice = input("> ").strip()
        
        try:
            if choice == "1":
                query = input("Search (title/author): ")
                books = search_books(data_dir, query)
                if books:
                    print("\n=== Search Results ===")
                    for book in books:
                        print(f"ISBN: {book.ISBN}, Title: {book.Title}, Author: {book.Author}, Available: {book.CopiesAvailable}")
                else:
                    print("No books found")
                    
            elif choice == "2":
                loans = get_member_loans(data_dir, member_id)
                if loans:
                    print("\n=== Your Loans ===")
                    for loan in loans:
                        status = "Returned" if loan.ReturnDate else f"Due on {format_date(loan.DueDate)}"
                        print(f"Loan ID: {loan.LoanID}, ISBN: {loan.ISBN}, Issued: {format_date(loan.IssueDate)}, Status: {status}")
                else:
                    print("No active loans")
                    
            elif choice == "3":
                logout()
                break
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()