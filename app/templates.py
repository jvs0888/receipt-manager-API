import os
from pathlib import Path
from fastapi.templating import Jinja2Templates

directory: str = os.path.join(Path(__file__).parent.parent, "templates")

templates: Jinja2Templates = Jinja2Templates(directory=directory, autoescape=False, auto_reload=True)
