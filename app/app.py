from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
import redis
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@postgres:5432/forum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

# Connect to Redis
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

# Define the User model for SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

# Database initialization
@app.before_first_request
def create_tables():
    db.create_all()

    # Add an example user
    example_user = User(username='example_user', password_hash=pbkdf2_sha256.hash('example_password'))
    db.session.add(example_user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

# Password hashing using passlib
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password_hash):
        return username

# Define a route for the home page
@app.route('/')
@auth.login_required
def home():
    # Access Redis
    redis_client.set('example_key', 'Hello, Redis!')
    redis_value = redis_client.get('example_key')

    # Access an external API using requests
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    api_data = response.json()

    return render_template('index.html', redis_value=redis_value, api_data=api_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)