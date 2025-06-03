import os
import requests

from flask import jsonify, request
from . import diease_bp
from ... utils.db_utils import *


@diease_bp.route('/list', methods=['GET'])
def list_diseases():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.diseases')
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@diease_bp.route('/add', methods=['POST'])
def add_disease():
    try:
        data = request.json
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.diseases (name, description) VALUES (%s, %s)', (data['name'], data['description']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Disease added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@diease_bp.route('/get_disease/{id}', methods=['GET'])
def get_disease(id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.diseases WHERE id = %s', (id,))
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@diease_bp.route('/get_user_diseases/{user_id}', methods=['GET'])
def get_user_diseases(user_id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.diseases WHERE user_id = %s', (user_id,))
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@diease_bp.route('/get_history_diseases/{history_id}', methods = ['GET'])
def get_history_diseases(history_id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.diseases WHERE history_id = %s', (history_id,))
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@diease_bp.route('/predict', methods=['POST'])
def predict_disease():
    
    try:
        data = request.json
        response = requests.post('http://localhost:5000/predict', json=data)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500