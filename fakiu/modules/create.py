from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from fakiu.models import Racer

bp = Blueprint('create', __name__, url_prefix='/create')

@bp.route('/racer', methods=('GET', 'POST'))
def racer():
    if request.method == 'POST':
        
        name = request.form['name']
        surname = request.form['surname']
        nickname = request.form['nickname']
        height = float(request.form['height']) if request.form['height'] else None
        weight = float(request.form['weight']) if request.form['weight'] else None
        picture = request.files.getlist('picture')[0]
        winner_picture = request.files.getlist('winner_picture')[0]
        serious_picture = request.files.getlist('serious_picture')[0]
        kart_picture = request.files.getlist('kart_picture')[0]

        picture_path = image_tools.file_handler(picture)
        winner_picture_path = image_tools.file_handler(winner_picture)
        serious_picture_path = image_tools.file_handler(serious_picture)
        kart_picture_path = image_tools.file_handler(kart_picture)

        racer = Racer(
            name=name, 
            surname=surname, 
            nickname=nickname, 
            height=height, 
            weight=weight,
            picture=picture_path, 
            winner_picture=winner_picture_path, 
            serious_picture=serious_picture_path, 
            kart_picture=kart_picture_path
            )
        racer.save()
        return redirect(url_for('index'))

    action = 'create/racer'

    fields = []
    fields.append({'type':'Text','label':'Name','name':'name','options':None,'required':True})
    fields.append({'type':'Text','label':'Surname','name':'surname','options':None,'required':True})
    fields.append({'type':'Text','label':'Nickname','name':'nickname','options':None,'required':False})
    fields.append({'type':'Float','label':'Height','name':'height','options':None,'required':False})
    fields.append({'type':'Float','label':'Weight','name':'weight','options':None,'required':False})
    fields.append({'type':'Picture','label':'Picture','name':'picture','options':None,'required':False})
    fields.append({'type':'Picture','label':'Winner Picture','name':'winner_picture','options':None,'required':False})
    fields.append({'type':'Picture','label':'Serious Picture','name':'serious_picture','options':None,'required':False})
    fields.append({'type':'Picture','label':'Kart Picture','name':'kart_picture','options':None,'required':False})

    button_name = 'Criar'

    form_info = {
        'action': action,
        'fields': fields,
        'button_name': button_name
    }
    return render_template('create/racer.html', form_info=form_info)
