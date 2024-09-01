from flask import Flask, request, jsonify
from models import db, Event

# Initialize Flask application
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# CRUD operations

# Create a new event
@app.route('/events', methods=['POST'])
def add_event():
    data = request.json
    new_event = Event(
        name=data.get('name'),
        location=data.get('location'),
        date=data.get('date'),
        description=data.get('description')
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully', 'event': {
        'id': new_event.id,
        'name': new_event.name,
        'location': new_event.location,
        'date': new_event.date,
        'description': new_event.description
    }}), 201

# Get all events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [{'id': event.id, 'name': event.name, 'location': event.location, 'date': event.date, 'description': event.description} for event in events]
    return jsonify(events_list), 200

# Get a single event by ID
@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify({
        'id': event.id,
        'name': event.name,
        'location': event.location,
        'date': event.date,
        'description': event.description
    }), 200

# Update an existing event
@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.json

    event.name = data.get('name', event.name)
    event.location = data.get('location', event.location)
    event.date = data.get('date', event.date)
    event.description = data.get('description', event.description)

    db.session.commit()
    return jsonify({'message': 'Event updated successfully', 'event': {
        'id': event.id,
        'name': event.name,
        'location': event.location,
        'date': event.date,
        'description': event.description
    }}), 200

# Delete an event
@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'}), 204

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
