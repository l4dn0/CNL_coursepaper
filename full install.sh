python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
curl -o ruwordnet.db http://raw.githubusercontent.com/avidale/python-ruwordnet/master/ruwordnet/static/ruwordnet.db