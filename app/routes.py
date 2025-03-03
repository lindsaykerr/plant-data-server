from flask import request, jsonify, render_template
from . import db
from .models import Data
from . import create_app

app = create_app()

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    value = data.get('value')
    if value is not None and 0 <= value <= 10:
        new_data = Data(value=value)
        db.session.add(new_data)
        db.session.commit()
        return jsonify({'message': 'Data submitted successfully'}), 201
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/data', methods=['GET'])
def get_data():
    data = Data.query.all()
    return jsonify([{'value': d.value, 'timestamp': d.timestamp} for d in data])

@app.route('/')
def index():
    return render_template('index.html')