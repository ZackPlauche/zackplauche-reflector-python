from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

STORAGE_DIRECTORY_NAME = 'Data Storage'

STORAGE_DIRECTORY = BASE_DIR / 'data' / (STORAGE_DIRECTORY_NAME if not DEBUG else 'Test Storage')

