import functools
import json
import sys
import csv
import os

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for , current_app , jsonify , render_template_string
from werkzeug.security import check_password_hash, generate_password_hash
import jinja2

from fakiu.models import *
from fakiu.tools import tools

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/edit/<model>/<id>', methods=('GET', 'POST'))
def edit(model,id):
    if request.method == 'POST':
        model = globals()[model]
        obj = model.query.filter_by(id=id).first()
        form = obj.get_edit_form()
        values = form.set_values(request)
        obj.update_with_dict(values)
        return jsonify(sucess=True)
    return jsonify(sucess=False)

@bp.route('/delete/<model>/<id>', methods=('GET', 'POST'))
def delete(model,id):
    model_name = model
    if request.method == 'POST':
        model = globals()[model]
        obj = model.query.filter_by(id=id).first()
        obj.delete()
        return jsonify(url_for('editor.display_all',model=model_name))
    return jsonify(sucess=False)

@bp.route('/query/<model>', methods=('GET', 'POST'))
def query(model):
    model = globals()[model]
    instances = model.query.order_by(model.creation_datetime.asc()).all()
    instances = [{'value':instance.id,'name':instance.name} for instance in instances]
    return jsonify(instances)

@bp.route('/remove_relationship', methods=('GET', 'POST'))
def remove_relationship():
    data = request.get_json()

    model_name1 = data.get('model_name1')
    model_name2 = data.get('model_name2')
    field_name = data.get('field_name')
    id1 = int(data.get('id1'))
    id2 = int(data.get('id2'))

    model1 = globals()[model_name1]
    model2 = globals()[model_name2]

    obj1 = model1.query.filter_by(id=id1).first()
    obj2 = model2.query.filter_by(id=id2).first()

    field = getattr(obj1,field_name)
    field.remove(obj2)
    obj1.save()
    return jsonify(sucess=True)

@bp.route('/modal_create_page/<model>', methods=('GET', 'POST'))
def modal_create_page(model):
    model_name = model
    model = globals()[model_name]
    empty_instance = model()
    form = empty_instance.get_basic_create_form()
    if request.method == 'POST':
        values = form.set_values(request)
        empty_instance.update_with_dict(values)
        empty_instance.create()
        response = {'value':empty_instance.id,'name':empty_instance.name}
        return jsonify(response)
    data = empty_instance.get_basic_create_data(form)
    return render_template('editor/modal_create.html',data = data)


@bp.route("/download_csv/<model>", methods =["GET", "POST"])
def download_csv(model):
    model_name = model
    model = globals()[model_name]
    filepath = tools.create_csv_for_model(model)
    return filepath


@bp.route("/upload_csv_to_db/<model>", methods =["GET", "POST"])
def upload_csv_to_db(model):
    model_name = model
    model = globals()[model_name]
    check = tools.upload_csv_to_model(model)
    if check:
        return jsonify(url_for('editor.display_all',model=model_name))
    else:
        return jsonify(sucess=False)

@bp.route('/race_results_creation_table/<int:number_of_rows>')
def get_race_results_creation_table(number_of_rows):
    html = render_template_string('{% from "macros/editor.html" import race_results_creation_table %}{{ race_results_creation_table(number_of_rows) }}', number_of_rows=number_of_rows)
    print()
    return jsonify({'html': html})

@bp.route('/race_results_creation_row/<int:index>/<int:number_of_rows>')
def get_new_rows_race_results_table(index,number_of_rows):
    html = render_template_string('{% from "macros/editor.html" import racer_row %}{% for i in range(number_of_rows) %}{{racer_row(i+1+index)}}{% endfor %}', index=index,number_of_rows=number_of_rows)
    return jsonify({'html': html})