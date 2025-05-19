python -m venv .venv
call .venv\Scripts\activate.bat
call pip install -r requirements.txt
call curl -o ruwordnet.db http://raw.githubusercontent.com/avidale/python-ruwordnet/master/ruwordnet/static/ruwordnet.db