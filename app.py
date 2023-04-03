from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Define the elevators
elevators = [
    {"id": 1, "floor": 1, "dest": None, "state": "stopped"},
    {"id": 2, "floor": 1, "dest": None, "state": "stopped"}
]

# Define the floors
floors = [
    {"id": 1, "elevator": None},
    {"id": 2, "elevator": None},
    {"id": 3, "elevator": None},
    {"id": 4, "elevator": None},
    {"id": 5, "elevator": None}
]

# API endpoints


@app.route('/call_elevator', methods=['POST'])
def call_elevator():
    # Get the floor number from the request
    floor = request.json['floor']

    # Find an available elevator
    elevator = None
    for e in elevators:
        if e['state'] == 'stopped':
            elevator = e
            break

    # If no elevator is available, return an error message
    if not elevator:
        return jsonify({'error': 'No elevators available'}), 400

    # Set the elevator's destination floor
    elevator['dest'] = floor

    # Assign the elevator to the requested floor
    floors[floor-1]['elevator'] = elevator['id']

    # Update the elevator's state
    elevator['state'] = 'moving'

    # Return a success message
    return jsonify({'message': f'Elevator {elevator["id"]} has been dispatched to floor {floor}'}), 200


@app.route('/get_elevators', methods=['GET'])
def get_elevators():
    # Return the current state of all elevators
    return jsonify({'elevators': elevators}), 200


@app.route('/set_destination', methods=['POST'])
def set_destination():
    # Get the elevator ID and destination floor from the request
    elevator_id = request.json['elevator']
    dest_floor = request.json['floor']

    # Find the elevator with the given ID
    elevator = None
    for e in elevators:
        if e['id'] == elevator_id:
            elevator = e
            break

    # If no elevator is found, return an error message
    if not elevator:
        return jsonify({'error': f'Elevator {elevator_id} not found'}), 404

    # Set the elevator's destination floor
    elevator['dest'] = dest_floor

    # Update the elevator's state
    elevator['state'] = 'moving'

    # Return a success message
    return jsonify({'message': f'Elevator {elevator_id} is now moving to floor {dest_floor}'}), 200


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
