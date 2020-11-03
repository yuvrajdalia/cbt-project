from flask import Flask,render_template,request
import pickle     # import flask
from web3 import Web3
from flask import jsonify
import json
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import sqlite3
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

app = Flask(__name__)

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
abi = json.loads('[ { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "citizen_array", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "", "type": "address" } ], "name": "citizens", "outputs": [ { "internalType": "string", "name": "city", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "count", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "_city", "type": "string" } ], "name": "fetchcity", "outputs": [ { "internalType": "address[]", "name": "", "type": "address[]" }, { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "bool[132]", "name": "_symptoms", "type": "bool[132]" } ], "name": "fill_symptoms", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "get_symptoms", "outputs": [ { "internalType": "bool[132]", "name": "_symptoms", "type": "bool[132]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "_city", "type": "string" } ], "name": "register_citizen", "outputs": [], "stateMutability": "nonpayable", "type": "function" } ]')
address=web3.toChecksumAddress("0x5E2A8030CCCE46B70107A14D2362816a772E3dd3")
contract = web3.eth.contract(address=address, abi=abi)
#web3.eth.defaultAccount = "0x6CB5DA51ba3F64566dA150e2BA2B231A7bF5C362"
public_key=""

@app.route("/")
def hello():
    arr_disease=['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']                      # call method hello
    return render_template('form.html',symptoms=arr_disease)


@app.route('/model', methods = ['POST', 'GET'])
def call_model():
    if request.method=='POST':
        print("hit")
        test_dict=request.form.to_dict()
        print(test_dict['img'])

        image =open('G:\\projects\\healthcare\\images\\'+str(test_dict['img']), 'r+b')
        print(image)
        
        KEY = 'bc24b9e0e54e4c96b4c59ccc5adfdea3'
        ENDPOINT = 'https://itprojectcbt.cognitiveservices.azure.com/'
        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        face_ids = []
        faces = face_client.face.detect_with_stream(image)
        for face in faces:
            face_ids.append(face.face_id)
        print("------")
        print(face_ids)
        print("------")
        # Identify faces
        results = face_client.face.identify(face_ids, 'test2')
        if(len(results[0].candidates)==0):
            return "You are not authorised to fill the survey"
        res=results[0].candidates[0].person_id
        connect = sqlite3.connect("Face-DataBase")
        c=connect.cursor()
        c.execute("SELECT * FROM Students WHERE personID = ?", (res,))
        row = c.fetchone()
        print(row[4])
        print(row[1] + " recognized")
        test_dict.pop('img')
        testcase=list(test_dict.values())
        print(type(testcase[0]))
        symptoms = []
        for i in range(0,len(testcase)):
            if testcase[i] != '':
                testcase[i]=int(testcase[i])
                if(testcase[i] == 1):
                    symptoms.append(True)
                else:
                    symptoms.append(False)
            else:
                symptoms.append(False)
                testcase[i] = 0
        print(testcase)
        arr=[]
        arr.append(testcase)
        arr.append(testcase)
        print(arr)
        filename='model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        prediction=loaded_model.predict(arr)
        print(prediction[0])
        print(len(symptoms))
        print(str(symptoms))
        print(row[4])
        web3.eth.defaultAccount =str(row[4])
        contract.functions.fill_symptoms(symptoms).transact()
        return "You suffer from " + prediction[0] +"."

@app.route('/geocity', methods = ['POST','GET'])
def geocity():
    if request.method == 'GET':
        cities = ["Mumbai", "Delhi", "Bangalore"]
        return render_template("city.html", cities=cities)
    if request.method == 'POST':
        print(request.form.get('city'))
        citizens, n = contract.functions.fetchcity(request.form.get('city')).call()
        print(citizens)
        print(n)
        final_matrix = []
        if n==0:
            return "No citizen in this city"
        if n is not 0:
            for i in range(n):
                web3.eth.defaultAccount = citizens[i]
                print(web3.eth.defaultAccount)
                tmp = []
                tmp = contract.functions.get_symptoms().call()
                print(tmp)
                tmp = [int(tm) for tm in tmp]
                final_matrix.append(tmp)
            print(final_matrix)
            filename='model.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            predictions = loaded_model.predict(final_matrix)
            print(predictions)
            names=[]
            for citizen in citizens:
                res=citizen
                connect = sqlite3.connect("Face-DataBase")
                c=connect.cursor()
                c.execute("SELECT * FROM Students WHERE Publickey = ?", (res,))
                row = c.fetchone()
                names.append(row[1])
                print(row[1])
            print(citizens)
            return render_template("geocity.html", citizens=citizens, predictions = predictions, city = request.form.get('city'),n=n,names=names)
        else:
            return "No person in this city"





if __name__ == "__main__":
    app.run()   