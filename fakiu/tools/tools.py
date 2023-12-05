import os
import csv

from flask import current_app, url_for

def create_csv_for_model(model):
    model_name = model.__name__.lower()
    instances = model.query.all()

    filename = f'data/csv/{model_name}.csv'
    file_path = current_app.root_path + url_for('static', filename = filename)
    instances = [instance.get_dict() for instance in instances]
    if instances:
        fieldnames = instances[0].keys() 

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in instances:
                writer.writerow(row)

    return url_for('static', filename = filename)
    