#!venv/bin/python
from app import app
app.secret_key = 'my precious'
app.database = 'notes.db'

if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0', 5000)
