from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

table = sqlite3.connect("database.db", check_same_thread=False)
cursor = table.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, score INTEGER)''')
table.commit()

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/submit', methods=['POST'])
def save():
	name = request.form['name-entry']
	iden = int(request.form['id-entry'])
	score = int(request.form['score-entry'])

	cursor.execute('''INSERT INTO users(id, name, score) VALUES(?, ?, ?)''', (iden, name, score))
	table.commit()

	print("Created user with ID:", iden, "Name:", name, "Score:", score)

	return redirect(request.referrer)

@app.route('/search', methods=['POST'])
def search():
	iden = int(request.form['id-search'])

	cursor.execute('''SELECT * FROM users WHERE id = ?''', (iden,))
	userData = cursor.fetchone()

	print("Fetched user with data:", userData)

	return redirect(request.referrer)

@app.route('/delete', methods=['POST'])
def delete():
	iden = int(request.form['id-delete'])

	cursor.execute('''DELETE FROM users WHERE id = ?''', (iden,))
	table.commit()

	print("Deleted user with ID:", iden)

	return redirect(request.referrer)

if __name__ == '__main__':
	app.run()
