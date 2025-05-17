import bcrypt
from typing import Optional, Dict
from .models import Member
from .storage import Storage

session: Dict[str, Optional[Member]] = {'current_user': None}

def register_member(data_dir: str, name: str, email: str, password: str, role: str = 'member') -> Member:
    members = Storage.read_csv(f"{data_dir}/members.csv", Member)
    new_id = str(max(int(m.MemberID) for m in members) + 1) if members else "1001"
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    member = Member(
        MemberID=new_id,
        Name=name,
        Email=email,
        PasswordHash=hashed.decode('utf-8'),
        Role=role
    )
    
    members.append(member)
    Storage.write_csv(f"{data_dir}/members.csv", members)
    return member

def login(data_dir: str, email: str, password: str) -> Optional[Member]:
    members = Storage.read_csv(f"{data_dir}/members.csv", Member)
    member = next((m for m in members if m.Email == email), None)
    
    if member and bcrypt.checkpw(password.encode('utf-8'), member.PasswordHash.encode('utf-8')):
        session['current_user'] = member
        return member
    return None

def logout():
    session['current_user'] = None

def get_current_user() -> Optional[Member]:
    return session.get('current_user')