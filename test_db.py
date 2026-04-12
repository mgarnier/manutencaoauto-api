from app import app
from manutencaoauto_api.db import init_db


init_db(app)
print('Database tables created successfully')