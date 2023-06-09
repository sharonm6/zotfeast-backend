import datetime
from flask import Blueprint, jsonify, request
from .utils import parse_schedule

calendar = Blueprint('api/calendar', __name__, url_prefix='/api/calendar')

@calendar.route('/parse', methods=['GET'])
def parse():
    ics_file = request.files.get('ics')
    date_str = request.args.get('date', default=None, type=str)

    if any(x is None for x in [ics_file, date_str]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        date = datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    return jsonify({'schedule': parse_schedule(ics_file, date)})