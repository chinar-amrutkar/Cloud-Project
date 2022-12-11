import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
import requests, json

db = firestore.client()
user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

@userAPI.route('/add', methods = ['POST'])
def create():
    try:
        data=request.json
        #print(data['id'])
        user_Ref.document(str(data['id'])).set(request.json)
        return jsonify({"Success": True}), 200
    except Exception as e:
        return f"An error eccured: {e}"


@userAPI.route('/list')
def read():
    try:
        all_users = [doc.to_dict() for doc in user_Ref.stream()] 
        return jsonify(all_users), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@userAPI.route('/bye/<id>', methods=['GET', 'DELETE'])
def delete(id):
    try:
        user_Ref.document(id).delete()
        return jsonify({"Success": True}), 200
    except Exception as e:
        return f"An error eccured: {e}"




@userAPI.route('/addCity', methods = ['POST'])
def createCity():
    try:
        data=request.json
        #print(data['id'])
        user_Ref.document(str(data['city'])).set(request.json)
        return jsonify({"Success": True}), 200
    except Exception as e:
        return f"An error eccured: {e}"

@userAPI.route('/temp/<city>')
def temperature(city):
    try:
        city_info = user_Ref.document(city).get().to_dict()
        lat = city_info['lat']
        long = city_info['long']
        temp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_180m&current_weather=true&start_date=2022-12-11&end_date=2022-12-11")
        contents = json.loads(temp.text)
        max_temp = max(contents['hourly']['temperature_180m'])
        min_temp = min(contents['hourly']['temperature_180m'])
        current_temp = contents['current_weather']['temperature']
        print(max_temp)
        print(min_temp)
        s = f"Today's forecast:\n\nCurrent temperature: {current_temp} \nMax temperature: {max_temp} \nMin temperature: {min_temp}"
        return s, 200
    except Exception as e:
        return f"An Error Occured: {e}"


