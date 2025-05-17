import random
import string
from datetime import datetime

def generate_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def format_date(date_str: str, format="%d-%b-%Y") -> str:
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime(format)