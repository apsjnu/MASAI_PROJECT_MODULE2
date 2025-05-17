from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Book:
    ISBN: str
    Title: str
    Author: str
    CopiesAvailable: int

@dataclass
class Member:
    MemberID: str
    Name: str
    Email: str
    PasswordHash: str
    Role: str  # 'member' or 'librarian'

@dataclass
class Loan:
    LoanID: str
    ISBN: str
    MemberID: str
    IssueDate: str
    DueDate: str
    ReturnDate: Optional[str] = None