from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

# Initialize elevator and floor states
elevators = [
    {"id": 1, "floor": 1, "dest": None, "state": "stopped"},
    {"id": 2, "floor": 1, "dest": None, "state": "stopped"}
]
floors = [
    {"id": 1, "elevator": None},
    {"id": 2, "elevator": None},
    {"id": 3, "elevator": None},
    {"id": 4, "elevator": None},
    {"id": 5, "elevator": None}
]

# Initialize logging
logging.basicConfig(filename='elevator.log', level=logging.DEBUG)

# API endpoint for calling an elevator from a specific floor


@app.route('/call_elevator', methods=['POST'])
def call_elevator():
    data = request.get_json()
    floor = data['floor']
    logging.info(f"Floor {floor} called an elevator")
    elevator = find_available_elevator()
    if elevator:
        assign_elevator_to_floor(elevator['id'], floor)
        return f"Elevator {elevator['id']} assigned to floor {floor}", 200
    else:
        logging.error("No available elevator found")
        return "No available elevator found", 400

# API endpoint for getting the current state of all elevators


@app.route('/get_elevators', methods=['GET'])
def get_elevators():
    return jsonify(elevators)

# API endpoint for setting the destination floor for a specific elevator


@app.route('/set_destination', methods=['POST'])
def set_destination():
    data = request.get_json()
    elevator_id = data['elevator_id']
    dest_floor = data['dest_floor']
    elevator = find_elevator_by_id(elevator_id)
    if elevator:
        elevator['dest'] = dest_floor
        logging.info(f"Elevator {elevator_id} set to go to floor {dest_floor}")
        return f"Elevator {elevator_id} set to go to floor {dest_floor}", 200
    else:
        logging.error(f"Elevator {elevator_id} not found")
        return f"Elevator {elevator_id} not found", 400

# Find an available elevator (i.e. an elevator that is currently stopped)


def find_available_elevator():
    for elevator in elevators:
        if elevator['state'] == "stopped":
            return elevator
    return None

# Assign an elevator to a specific floor


def assign_elevator_to_floor(elevator_id, floor):
    for elevator in elevators:
        if elevator['id'] == elevator_id:
            elevator['dest'] = floor
            floors[floor-1]['elevator'] = elevator_id
            logging.info(f"Elevator {elevator_id} assigned to floor {floor}")
            break

# Find an elevator by its ID


def find_elevator_by_id(elevator_id):
    for elevator in elevators:
        if elevator['id'] == elevator_id:
            return elevator
    return None


if __name__ == '__main__':
    app.run(debug=True)
