from datetime import datetime
import os
from flask import Blueprint, jsonify, request
from .utils import parse_schedule

calendar = Blueprint('api/calendar', __name__, url_prefix='/api/calendar')

@calendar.route('/parse', methods=['GET'])
def parse():
    # ics = request.args.get('ics', type=str)
    date_str = request.args.get('date', type=str)

    if any(x is None for x in [date_str]):
    # if any(x is None for x in [ics, date_str]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        date = datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    print(date_str)

    # return jsonify({'schedule': parse_schedule(ics, date)})
    return jsonify({'schedule': '102201'})