from dotenv import load_dotenv
import os

from fastapi.templating import Jinja2Templates

load_dotenv()

USER_EMAIL = os.environ.get("USER_EMAIL")
GOOGLE_SHEET = os.environ.get("GOOGLE_SHEET")

templates = Jinja2Templates(directory="src/templates")

