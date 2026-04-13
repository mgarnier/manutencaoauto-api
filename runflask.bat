@echo off
call .\venv_manutencaoauto-api\Scripts\activate.bat
set FLASK_APP=app:app
py -m flask run --host 0.0.0.0 --port 5000 --reload