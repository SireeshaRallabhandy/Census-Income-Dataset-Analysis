from flask import Flask,render_template, request, make_response
from wtforms import SelectField
from flask_wtf import FlaskForm 
from os import urandom
import os
import pickle
import pandas as pd
import json
from predictor import predict_income,get_values

filename = "Income_Predictor.pkl"
lo_mo = pickle.load(open(filename,'rb'))

app = Flask(__name__)

# @app.route('/',methods=['GET'])
# def hello_world():
#     return render_template("index.html")



SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class Form(FlaskForm):
    
    # age = SelectField("Age",choices = [range(18,120)])
    work_class = SelectField('Work Class', choices=[(3,'Private'), (5 , 'Self-emp-not-inc'), (4,'Self-emp-inc'), (0,'Federal-gov'),(1,'Local-gov'), (6,'State-gov'), (7,'Without-pay'), (2,'Never-worked')]) 
    education = SelectField('Education', choices=[(0,' Bachelors'), (4,'Some-college'), (2,'11th'), (2,'HS-grad'), (4,'Prof-school'), (4,'Assoc-acdm'), (4,'Assoc-voc'), (2,'9th'), (2,'7th-8th'), (2,'12th'),(3, 'Masters'), (2,'1st-4th'), (2,'10th'), (1,'Doctorate'), (2,'5th-6th'), (2,'Preschool')])
    marital_status = SelectField('Marital Status',choices = [(2,'Married-civ-spouse'), (1,'Divorced'), (0,'Never-married'), (1,'Separated'), (1,'Widowed'), (1,'Married-spouse-absent'), (2,'Married-AF-spouse')])
    occupation = SelectField('Occupation',choices= [(12,'Tech-support'),(2,'Craft-repair'), (7,'Other-service'), (11,'Sales'), (3,'Exec-managerial'), (9,'Prof-specialty'), (5,'Handlers-cleaners'), (6,'Machine-op-inspct'), (0,'Adm-clerical'), (4,'Farming-fishing'), (13,'Transport-moving'), (8,'Priv-house-serv'), (10,'Protective-serv'), (1,'Armed-Forces')])
    relationship = SelectField("Relationship",choices = [(0,'Husband'),(1,'Not-in-family'),(3,'Own-child'),(4,'Unmarried'),(5,'Wife'),(2,'Other-relative')])
    race = SelectField("Race",choices = [(4,'White'),(2,'Black'),(1,'Asian-Pac-Islander'),(0,'Amer-Indian-Eskimo'),(3,'Other')])
    sex = SelectField("Sex",choices=[(1,'Male'),(0,'Female')])
    native_country = SelectField("Native Country", choices = [(38,'United-States'), (3,'Cambodia'), (8,'England'), (32,'Puerto-Rico'), (1,'Canada'), (10,'Germany'), (27,'Outlying-US(Guam-USVI-etc)'), (18,'India'), (23,'Japan'), (11,'Greece'), (34,'South'), (2,'China'), (4,'Cuba'), (19,'Iran'), (15,'Honduras'), (29,'Philippines'), (21,'Italy'), (30,'Poland'), (22,'Jamaica'), (39,'Vietnam'), (25,'Mexico'), (31,'Portugal'), (20,'Ireland'), (9,'France'), (5,'Dominican-Republic'), (24,'Laos'), (6,'Ecuador'), (35,'Taiwan'), (13,'Haiti'), (3,'Columbia'), (17,'Hungary'), (12,'Guatemala'), (26,'Nicaragua'), (33,'Scotland'), (36,'Thailand'), (40,'Yugoslavia'), (7,'El-Salvador'), (37,'Trinadad&Tobago'), (28,'Peru'), (16,'Hong'), (14,'Holand-Netherlands')])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    return render_template('index.html', form=form)

@app.route('/pred/', methods=['GET', 'POST'])

def data():

    if request.method == 'GET':
        return render_template('redirect.html')

    if request.method == 'POST':
        age = int(request.form.get("age"))
        w_c = int(request.form.get("work_class"))
        fnlwgt = int(request.form.get("fnlwgt"))
        edu = int(request.form.get("education"))
        edu_num = int(request.form.get("education_num"))
        m_s = int(request.form.get("marital_status"))
        occu = int(request.form.get("occupation"))
        rel = int(request.form.get("relationship"))
        race = int(request.form.get("race"))
        sex = int(request.form.get("sex"))
        c_g = int(request.form.get("capital_gain"))
        c_l = int(request.form.get("capital_loss"))
        hpw = int(request.form.get("hours_per_week"))
        n_c = int(request.form.get("native_country"))
        prediction = predict_income(age, w_c, fnlwgt, edu, edu_num, m_s, occu, rel, race, sex, c_g, c_l, hpw, n_c)
        pred = max(prediction, key=lambda x: prediction[x])
        return render_template('data.html', pred=pred)

# @app.route('/', methods=['GET', 'POST'])

# def data():
#     if request.method == 'GET':
#         return render_template('redirect.html')
#     if request.method == 'POST':
#         age=int(request.form.get("age"))
#         w_c=int(request.form.get("work_class"))
#         fnlwgt=int(request.form.get("fnlwgt"))
#         edu=int(request.form.get("education"))
#         edu_num=int(request.form.get("education_num"))
#         m_s=int(request.form.get("marital_status"))
#         occu=int(request.form.get("occupation"))
#         rel=int(request.form.get("relationship"))
#         race=int(request.form.get("race"))
#         sex=int(request.form.get("sex"))
#         c_g=int(request.form.get("capital_gain"))
#         c_l=int(request.form.get("capital_loss"))
#         hpw=int(request.form.get("hours_per_week"))
#         n_c=int(request.form.get("native_country"))
#         prediction = predict_income(age,w_c,fnlwgt,edu,edu_num,m_s,occu,rel,race,sex,c_g,c_l,hpw,n_c)
#         pred = max(prediction, key=lambda x: prediction[x])
#         predi = make_response(pred)
#         return predi

if __name__ == "main":
    app.run(port = 3000, debug = True)













