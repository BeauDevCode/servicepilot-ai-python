from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.utils import human_date, money, parse_line_items, split_lines

templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))
templates.env.filters["money"] = money
templates.env.filters["date"] = human_date
templates.env.filters["line_items"] = parse_line_items
templates.env.filters["split_lines"] = split_lines

