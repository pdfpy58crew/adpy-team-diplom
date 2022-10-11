from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

G_TOKEN = os.getenv('G_TOKEN')
G_ID = os.getenv('G_ID')
U_TOKEN = os.getenv('U_TOKEN')

BD_USER = os.getenv('user')
BD_PASSWORD = os.getenv('password')
BD_NAME = os.getenv('bdname')