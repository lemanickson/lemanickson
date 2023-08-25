from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Replace 'your_database_file.db' with the path to your SQLite database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_file.db'
db = SQLAlchemy(app)

# Create a User model to store user information in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        # If the user exists in the database and the password matches,
        # redirect to the interface page and pass the username as a parameter
        return redirect(url_for('interface', username=username))
    else:
        return "Invalid login credentials. Please try again."

@app.route('/interface/<username>')
def interface(username):
    # Render the interface page and pass the username to personalize the content
    return render_template('interface.html', username=username)

if __name__ == '__main__':
    # Create the database tables if they don't exist
    if not os.path.exists('your_database_file.db'):
        db.create_all()

    app.run(debug=True)
