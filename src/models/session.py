from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Session:
    session_id: int
    user_id: Optional[int] = None
    token: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    expires_at: Optional[int] = None
    revoked_at:Optional[datetime] = None