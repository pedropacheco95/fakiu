from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from fakiu.tools import auth_tools

from fakiu.models import *

bp = Blueprint('editor', __name__, url_prefix='/editor')

@bp.before_request
@auth_tools.admin_required
def before_request():
    pass

@bp.route('/', methods=('GET', 'POST'))
def index():
    apps = Backend_App.query.all()
    apps = [app.get_dict() for app in apps] 
    return render_template('editor/index.html',page='editor_index',apps=apps)

@bp.route('/display/<model>', methods=('GET', 'POST'))
def display_all(model):
    page = f'editor_{model}_all'
    model = globals()[model]
    empty_instance = model()
    data = empty_instance.get_display_all_data()
    return render_template('editor/display_all.html', page=page, data=data)

@bp.route('/display/<model>/<id>', methods=('GET', 'POST'))
def display(model,id):
    page = f'editor_{model}'
    model = globals()[model]
    instance = model.query.filter_by(id=id).first()
    data = instance.get_display_data()
    return render_template('editor/display.html', page=page, data=data)

@bp.route('/create/<model>', methods=('GET', 'POST'))
def create(model):
    page = f'editor_{model}_create'
    model_name = model
    model = globals()[model_name]
    empty_instance = model()
    form = empty_instance.get_create_form()
    if request.method == 'POST':
        values = form.set_values(request)
        empty_instance.update_with_dict(values)
        empty_instance.create()
        return redirect(url_for('editor.display_all',model=model_name))
    data = empty_instance.get_create_data(form)
    return render_template('editor/create.html', page=page, data=data)

@bp.route('/kanban', methods=('GET', 'POST'))
def kanban():
    model = 'User'
    page = 'editor_kanban'
    page = f'editor_{model}_all'
    model = globals()[model]
    empty_instance = model()
    data = empty_instance.get_display_all_data()
    return render_template('editor/kanban.html',page=page, data=data)

@bp.route('/create_race_results/<model_name>/<model_id>', methods=('GET', 'POST'))
def create_race_results(model_name,model_id):
    page = f'editor_{model_name}_create'
    model = globals()[model_name]
    race = model.query.filter_by(id=model_id).first()
    if race.results_added:
        return redirect(url_for('editor.display',model=model_name,id=model_id))
    form = race.get_create_form()
    if request.method == 'POST':

        if race.results_added:
            raise Exception('The results were already added')

        points = RacePointDistribution.query.filter_by(championship_id=race.championship.id).all()
        points_dict = [point.get_points_dict() for point in points]
        points_dict = {k: v for d in points_dict for k, v in d.items()}
        racers = [int(ele) for ele in request.form.getlist('racer')]
        racer_places = [int(ele) for ele in request.form.getlist('racerPlace')]
        qualification = [int(ele) if ele else 0 for ele in request.form.getlist('qualification')]
        fastest_lap = [ele=='true' for ele in request.form.getlist('fastest_lap')]
        results = zip(racers, racer_places,qualification,fastest_lap)
        for item in results:
            racer_id = item[0]
            place = item[1]
            qualification_place = item[2]
            fastest_lap_flag = item[3]
            
            association_rr = Association_RacerRace(
                racer_id=racer_id, 
                race_id=race.id, 
                place=place, 
                qualification_place=qualification_place, 
                fastest_lap=fastest_lap_flag
            )
            association_rr.create(points_dict)

            if not Association_RacerTrack.query.filter_by(racer_id=racer_id, track_id=race.track.id).first():
                association_rt = Association_RacerTrack(racer_id=racer_id, track_id=race.track.id)
                association_rt.create()
            
            if not Association_RacerRestaurant.query.filter_by(racer_id=racer_id, restaurant_id=race.restaurant.id).first():
                association_rt = Association_RacerRestaurant(racer_id=racer_id, restaurant_id=race.restaurant.id)
                association_rt.create()

        all_championship_racers = [racer.id for racer in race.championship.racers]
        participating_racers = [int(racer) for racer in racers]
        non_participating_racers = set(all_championship_racers) - set(participating_racers)
        for racer_id in non_participating_racers:
            # Assign a punishment point or another indicator for non-participation
            association = Association_RacerRace(
                racer_id=racer_id, 
                race_id=race.id, 
                place=0, 
                qualification_place=0, 
            )
            association.create(points_dict)

        race.results_added = True
        return redirect(url_for('editor.display',model=model_name,id=race.id))
    data = race.get_create_data(form)

    data['post_url'] =  url_for('editor.create_race_results', model_name=model_name,model_id=model_id)

    return render_template('editor/special_creation_pages/races.html', page=page, data=data)