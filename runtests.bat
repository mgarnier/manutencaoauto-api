@echo off
call .\venv_manutencaoauto-api\Scripts\activate.bat
py -m unittest discover -s tests -p "test_*.py" -v