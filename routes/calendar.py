from datetime import datetime
import json
import os
from flask import Blueprint, jsonify, request
from .utils import parse_schedule

calendar = Blueprint('api/calendar', __name__, url_prefix='/api/calendar')

@calendar.route('/parse', methods=['POST'])
def parse():
    data = request.get_json()
    ics = data.get('ics', '')
    date_str = data.get('date', '')

    if any(x is None for x in [ics, date_str]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        date = datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    return jsonify({'schedule': parse_schedule(ics, date)});