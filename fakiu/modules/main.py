from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from fakiu.models import *

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    last_championship = Championship.query.order_by(Championship.creation_datetime.desc()).first()
    data = {'championship':last_championship}
    return render_template('index.html',data=data)

@bp.route('/calendar', methods=('GET','POST'))
def calendar():
    last_championship = Championship.query.order_by(Championship.creation_datetime.desc()).first()
    data = {'championship':last_championship}
    return render_template('calendar.html',data=data)

@bp.route('/grid', methods=('GET','POST'))
def grid():
    last_championship = Championship.query.order_by(Championship.creation_datetime.desc()).first()
    data = {'championship':last_championship}
    return render_template('grid.html',data=data)

@bp.route('/substitute_racers', methods=('GET','POST'))
def substitute_racers():
    racers = Racer.query.all()
    last_championship = Championship.query.order_by(Championship.creation_datetime.desc()).first()
    racers = [racer for racer in racers if racer not in last_championship.racers]
    racers_table = [{'racer':racer,'points':sum([rel.total_points for rel in racer.races_relations])} for racer in racers]
    championship_table_sorted = sorted(racers_table, key=lambda x: x['points'], reverse=True)
    for index, entry in enumerate(championship_table_sorted, start=1):
        entry['place'] = index
    data = {'racers':championship_table_sorted}
    return render_template('substitute_racers.html',data=data)


@bp.route('/racers', methods=('GET','POST'))
def racers():
    racers = Racer.query.all()
    data = {'racers':racers}
    return render_template('racers.html',data=data)

@bp.route('/racer/<id>', methods=('GET','POST'))
def racer(id):
    racer = Racer.query.filter_by(id=id).first()
    data = {'racer':racer}
    return render_template('racer.html',data=data)
