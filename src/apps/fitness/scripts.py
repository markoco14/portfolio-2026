import pandas

from src.config import GOOGLE_SHEET, USER_EMAIL
from src.database import get_conn

def get_google_sheet_data():
    df = pandas.read_csv(GOOGLE_SHEET)

    return df.values.tolist()

def format_for_db(rows):

    insert_rows = []
    for row in rows[:793]:
        new_row = {
            "date": pandas.to_datetime(row[1]).strftime("%Y-%m-%d"), 
            "distance": row[2], 
            "units": "km"
            }
        insert_rows.append(new_row)

    return insert_rows

def insert_data(insert_rows):
    with get_conn() as conn:
        user = conn.execute("SELECT user_id FROM users WHERE email = :email;",
                            {"email": USER_EMAIL}).fetchone()
        if not user:
            print("error getting user")
        else:
            for row in insert_rows:
                row["user_id"] = user["user_id"]

            cursor = conn.executemany(
                "INSERT OR IGNORE INTO runs (user_id, date, distance, units) VALUES (:user_id, :date, :distance, :units);",
                insert_rows
                )
            
            conn.commit()

            print(f"Successfully inserted {cursor.rowcount} new runs.")

def migrate_google_sheet_data():
    sheet_data = get_google_sheet_data()
    insert_rows = format_for_db(sheet_data)
    insert_data(insert_rows=insert_rows)

migrate_google_sheet_data()