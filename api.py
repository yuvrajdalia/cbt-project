from flask import Flask,render_template,request
import pickle     # import flask
from web3 import Web3
from flask import jsonify
import json
app = Flask(__name__)             # create an app instance

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
abi = json.loads('[ { "constant": false, "inputs": [ { "name": "_symptoms", "type": "bool[133]" } ], "name": "fill_symptoms", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "get_symptoms", "outputs": [ { "name": "symptoms", "type": "bool[133]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "citizens", "outputs": [ { "name": "latitude", "type": "string" }, { "name": "longitude", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_latitude", "type": "string" }, { "name": "_longitude", "type": "string" } ], "name": "register_citizen", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "citizen_array", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')
address=web3.toChecksumAddress("0xd88eBF317c7CD9EcB39EDbb79265B9facD2331e5")
contract = web3.eth.contract(address=address, abi=abi)

@app.route("/")                   # at the end point /
def hello():
    arr_disease=['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']                      # call method hello
    return render_template('form.html',symptoms=arr_disease)
    #return "Hello World!"         # which returns "hello world"


@app.route('/model', methods = ['POST', 'GET'])
def call_model():
    if request.method=='POST':
        print("hit")
        test_dict=request.form.to_dict()
        testcase=list(test_dict.values())
        print(type(testcase[0]))
        symptoms = []
        for i in range(0,len(testcase)):
            testcase[i]=int(testcase[i])
            if(testcase[i] == 1):
                symptoms.append(True)
            else:
                symptoms.append(False)
        print(testcase)
        arr=[]
        arr.append(testcase)
        arr.append(testcase)
        print(arr)
        filename='model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        prediction=loaded_model.predict(arr)
        print(prediction[0])
        web3.eth.defaultAccount = "0xa6D9B0B5970AEDc6c64D3a0767af7df84266F912"
        print(len(symptoms))
        print(str(symptoms))
        contract.functions.fill_symptoms(symptoms).transact()
        return "You suffer from " + prediction[0] +"."

@app.route('/fetchsymptoms', methods = ['POST','GET'])
def fetchsymptoms():
    web3.eth.defaultAccount = "0xa6D9B0B5970AEDc6c64D3a0767af7df84266F912"
    if request.method == 'GET':
        cities = ["Indore", "Amritsar", "Bangalore"]
        return render_template("city.html", cities=cities)
        # medicines = contract.functions.get_symptoms().call()
        # return jsonify({"medicines":str(medicines)})





if __name__ == "__main__":        # on running python app.py
    app.run()   