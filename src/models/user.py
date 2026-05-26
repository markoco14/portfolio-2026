from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    user_id: int
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None