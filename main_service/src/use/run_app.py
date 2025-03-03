from dotenv import load_dotenv

from use.main.setup import create_app

load_dotenv()

app = create_app()
