from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Run:
    run_id: int
    user_id: Optional[int] = None
    activity_date: Optional[date] = None
    distance: Optional[float] = None 
    units: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None