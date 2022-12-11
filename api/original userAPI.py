import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()
user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

@userAPI.route('/add', methods = ['POST'])
def create():
    try:
        id = uuid.uuid4()
        user_Ref.document(id.hex).set(request.json)
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
        todo_id = request.args.get(id)
        user_Ref.document(todo_id).delete()
        return jsonify({"Success": True}), 200
    except Exception as e:
        return f"An error eccured: {e}"