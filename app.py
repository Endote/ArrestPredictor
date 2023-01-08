# Based on PhD Yash Modi work
import flask
import os
import pandas as pd
import pickle
import uuid
import urllib

from flask import Flask , make_response, render_template  , request , send_file



app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

def predict(variables):
    predictions = loaded_model.predict([variables])
    return predictions

def map_driver_race(race):
    race_dict = {'White': 0, 'Black': 1, 'Asian': 2, 'Hispanic': 3, 'Other': 4}
    return race_dict[race]

def map_driver_gender(gender):
    gender_dict = {'M': 0, 'F': 1}
    return gender_dict[gender]

def map_bool(boolean):
    boolean_dict = {'True': 1, 'False': 0}
    return boolean_dict(boolean)

def map_time(t):
    x = None
    y = None
    return x * 60 + y

def map_violation(violation):
    violation_dict = {'Speeding': 0,
            'Other': 1,
            'Equipment': 2,
            'Moving violation': 3,
            'Registration/plates': 4}
    return violation_dict[violation]

def map_variables(variables):
    
    return None

def time_to_int(x):
    tmp = str(x).split(':')
    res = (int(tmp[0]) if tmp[0] != '00' else 0) * 60 + (int(tmp[1]) if tmp[1] != '00' else 0)
    return res

@app.route('/', methods = ['GET' , 'POST'])
def home():
    if request.method == 'GET':
        response = make_response( render_template("index.html"), 200)
        return response

    elif request.method == 'POST':

        if request.form.get('x1') is not None and request.form.get('x2') is not None and request.form.get('x3') is not None and request.form.get('x4') is not None and request.form.get('x5') is not None and request.form.get('x6') is not None and request.form.get('x7') is not None: 
            if not request.form.get('x1') and not request.form.get('x2'):
                return render_template("index.html")

            variables = [time_to_int(request.form.get('x1')), int(request.form.get('x2')), request.form.get('x3'), request.form.get('x4'), request.form.get('x5'),request.form.get('x6'),request.form.get('x7')]
            
            predictions = predict(variables)

            pred = "You will be arrested" if predictions[0]==1 else "You won't be arrested"
            result = {'y' : pred}

            response = make_response( render_template("index.html", **result), 203)
            return response

        else:
            
            response = make_response( render_template("index.html"), 200)
            return response
    
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True)


