import os, json
from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
from .models import Task, User

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)

INCOMING_DATE_FMT = '%d/%m/%Y %H:%M:%S'

@app.route('/')
def hello_world():
  return 'Hello World'

@app.route('/api/v1/', methods=["GET"])
def info_view():
  """List of routes for this API."""
  output = {
      'info': 'GET /api/v1',
      'register': 'POST /api/v1/accounts',
      'single profile detail': 'GET /api/v1/accounts/<username>',
      'edit profile': 'PUT /api/v1/accounts/<username>',
      'delete profile': 'DELETE /api/v1/accounts/<username>',
      'login': 'POST /api/v1/accounts/login',
      'logout': 'GET /api/v1/accounts/logout',
      "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
      'create task': 'POST /api/v1/accounts/<username>/tasks',
      'task detail': 'GET /api/v1/accounts/<username>/tasks/<id>',
      'task update': 'PUT /api/v1/accounts/<username>/tasks/<id>',
      'delete task': 'DELETE /api/v1/accounts/<username>/tasks/<id>'
  }
  return jsonify(output)

@app.route('/api/v1/accounts/<username>/tasks', methods=['POST'])
def create_task(username):
  """Create a task for one user."""
  user = User.query.filter_by(username=username).first()
  if user:
    task = Task(
      name=request.form['name'],
      note=request.form['note'],
      creation_date=datetime.now(),
      due_date=datetime.strptime(due_date, INCOMING_DATE_FMT) if due_date else None,
      completed=bool(request.form['completed']),
      user_id=user.id,
    )
    db.session.add(task)
    db.session.commit()
    output = {'msg': 'posted'}
    response = Response(
      mimetype="application/json",
      response=json.dumps(output),
      status=201
    )
    return response

