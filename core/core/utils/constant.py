import os
from dotenv import load_dotenv

load_dotenv()

NAME=os.getenv('NAME')
DBUSER=os.getenv('DBUSER')
PASSWORD=os.getenv('PASSWORD')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')

MANAGER = 'manager'
USER = 'user'
PUBLIC = 'PUBLIC'
ADMIN = 'admin'
ALL_ROLES = [MANAGER, USER, PUBLIC, ADMIN]
