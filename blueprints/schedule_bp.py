import flask

blueprint = flask.Blueprint('schedule_blueprint', __name__, template_folder='templates')


@blueprint.route('/schedule', methods=['GET', 'POST'])
def schedule():
    pass
