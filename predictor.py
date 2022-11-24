from flask import Flask,render_template, request, jsonify
from wtforms import SelectField
from flask_wtf import FlaskForm 
from os import urandom
import os
import pickle
import pandas as pd
import pickle
import pandas as pd

filename = "Income_Predictor.pkl"
lo_mo = pickle.load(open(filename,'rb'))

def get_values():
    values = []
    for value in request.form.values():
        values.append(int(value))
        print(jsonify(values))
    return jsonify(values)


def predict_income(age, work_class, fnlwgt, education, education_num, marital_status, occupation,relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country):
    df_new = pd.DataFrame.from_dict({'age':[age], 'workclass':[work_class], 'fnlwgt':[fnlwgt], 'education':[education], 'education-num':education_num, 'marital-status':[marital_status], 'occupation':[occupation],'relationship':[relationship], 'race':[race], 'sex':[sex], 'capital-gain':[capital_gain], 'capital-loss':[capital_loss], 'hours-per-week':[hours_per_week], 'native-country':[native_country]})
    pred = lo_mo.predict_proba(df_new)[0]
    return {'<=50K': pred[0], '>50K': pred[1]}
