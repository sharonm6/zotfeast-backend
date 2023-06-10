from flask import Blueprint, jsonify, request
from .utils import get_recommendation, calc_distance

recommendation = Blueprint('api/recommendation', __name__, url_prefix='/api/recommendation')

@recommendation.route('/notification', methods=['GET'])
def notification():
    schedule = request.args.get('schedule', default=None, type=str)
    time = request.args.get('time', default=None, type=int)
    dist = request.args.get('dist', default=None, type=float)
    task = request.args.get('task', default=None, type=int)
    duration = request.args.get('duration', default=None, type=float)
    if any(x is None for x in [schedule, time, dist, task, duration]):
        return jsonify({'error': 'Missing required parameters'}), 400
    return jsonify({'notification': get_recommendation(schedule, time, dist, task, duration)})

@recommendation.route('/distance', methods=['GET'])
def distance():
    latitude = request.args.get('latitude', default=None, type=str)
    longitude = request.args.get('longitude', default=None, type=int)
    task = request.args.get('task', default=None, type=float)

    if any(x is None for x in [latitude, longitude, task]):
        return jsonify({'error': 'Missing required parameters'}), 400
    return jsonify({'distance': calc_distance(latitude, longitude, task)})
