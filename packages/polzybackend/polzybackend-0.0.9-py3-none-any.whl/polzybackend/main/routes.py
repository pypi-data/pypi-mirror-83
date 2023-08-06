from flask import jsonify, request
from datetime import date
from ..policy import Policy
from ..models import Activity, ActivityType
from ..utils import get_policy_class, get_activity_class
from . import bp
from fasifu.GlobalConstants import GlobalConstants
from logging import getLogger

logger = getLogger(GlobalConstants.loggerName)


@bp.route('/policy/<string:policy_number>/<string:effective_date>')
@bp.route('/policy/<string:policy_number>')
def get_policy(policy_number, effective_date=None):
    #
    # fetches a Policy by policy_number & effective_data
    # and returns it
    #

    # set default effective_date if needed
    if effective_date is None:
        effective_date = str(date.today())

    try:
        # get Policy
        policy = get_policy_class()(policy_number, effective_date)
        if policy.fetch():
            return jsonify(policy.get()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Policy not found'}), 404


@bp.route(f'/activity', methods=['POST'])
def new_activity():
    #
    # create new activity
    #

    # get post data
    data = request.get_json()

    # create activity
    try:
        #activity = Activity.create_from_json(data)
        activity = get_activity_class(data.get('activity_class')).create_from_json(data)
        
    except Exception as e:
        print(e)
        return jsonify({'error': 'Bad Request'}), 400

    # TODO: execute activity
    lString = activity.executeActivity()
    logger.info(f"String returned from {activity.__class__} was: {lString}")

    return jsonify({
        'id': str(lString),
        'status': 'accepted',
        'msg': 'Activity accepted',
    }), 202
