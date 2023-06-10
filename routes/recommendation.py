from flask import Blueprint, jsonify, request
from .utils import get_recommendation
from .utils import calc_distance

recommendation = Blueprint('api/recommendation', __name__, url_prefix='/api/recommendation')

@recommendation.route('/notification', methods=['POST'])
def notification():
    data = request.get_json()
    schedule = data.get('schedule', '')
    time = data.get('time', '')
    dist = data.get('dist', '')
    task = data.get('task', '')
    duration = data.get('duration', '')

    if any(x is None for x in [schedule, time, dist, task, duration]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    return jsonify({'notification': get_recommendation(schedule, time, dist, task, duration)})

@recommendation.route('/distance', methods=['POST'])
def distance():
    data = request.get_json()
    latitude = data.get('latitude', '')
    longitude = data.get('longitude', '')
    task = data.get('task', '')

    if any(x is None for x in [latitude, longitude, task]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    return jsonify({'distance': calc_distance(latitude, longitude, task)})
