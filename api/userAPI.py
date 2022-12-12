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
        s = f"Today's forecast:\n\nCurrent temperature: {current_temp} \nMax temperature: {max_temp} \nMin temperature: {min_temp}"
        return s, 200
    except Exception as e:
        return f"An Error Occured: {e}"


@userAPI.route('/wind/<city>')
def wind_speed(city):
    try:
        city_info = user_Ref.document(city).get().to_dict()
        lat = city_info['lat']
        long = city_info['long']
        temp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=windspeed_180m,winddirection_180m&current_weather=true&start_date=2022-12-11&end_date=2022-12-11")
        contents = json.loads(temp.text)
        max_wind = max(contents['hourly']['windspeed_180m'])
        min_wind = min(contents['hourly']['windspeed_180m'])
        current_wind = contents['current_weather']['windspeed']
        s = f"Today's forecast:\n\nCurrent windspeed: {current_wind} \nMax windspeed: {max_wind} \nMin windspeed: {min_wind}"
        return s, 200
    except Exception as e:
        return f"An Error Occured: {e}"


@userAPI.route('/shouldIGoOut/<city>')
def smart_assist(city):
    try:
        city_info = user_Ref.document(city).get().to_dict()
        lat = city_info['lat']
        long = city_info['long']
        temp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=windspeed_180m,winddirection_180m&current_weather=true&start_date=2022-12-11&end_date=2022-12-11")
        contents = json.loads(temp.text)
        current_wind = contents['current_weather']['windspeed']
        current_temp = contents['current_weather']['temperature']

        
        
        temp_ok = "The temperature is not ideal today, maybe tomorrow!" if current_temp <10 or current_temp > 30 else "Perfect day to go out for an adventure!"
        wind_ok = "You'll enjoy a nice breeze today!" if current_wind <15 else "Too windy, better stay indoors!"

        
        s = f"Today's forecast:\n\n{temp_ok} \n{wind_ok}"
        return s, 200
    except Exception as e:
        return f"An Error Occured: {e}"


