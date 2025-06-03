import os
import requests

from flask import jsonify, request
from . import histories_bp
from ... utils.db_utils import *

@histories_bp.route('/list', methods=['GET'])
def list_histories():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.histories')
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@histories_bp.route('/add', methods=['POST'])
def add_history():
    try:
        data = request.json
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.histories (user_id, disease_id, date) VALUES (%s, %s, %s)', (data['user_id'], data['disease_id'], data['date']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'History added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@histories_bp.route('/histories/{id}', methods=['GET'])
def get_history(id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.histories WHERE id = %s', (id,))
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@histories_bp.route('/get_user_histories/{user_id}', methods=['GET'])
def get_user_histories(user_id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.histories WHERE user_id = %s', (user_id,))
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@histories_bp.route('/get_disease_histories/{disease_id}', methods=['GET'])

def get_disease_histories(disease_id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.histories WHERE disease_id = %s', (disease_id,))
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@histories_bp.route('/get_user_disease_histories/{user_id}/{disease_id}', methods=['GET'])
def get_user_disease_histories(user_id, disease_id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.histories WHERE user_id = %s AND disease_id = %s', (user_id, disease_id))
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@histories_bp.route('/get_user_disease_histories_count/{user_id}/{disease_id}', methods=['GET'])
def get_user_disease_histories_count(user_id, disease_id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM public.histories WHERE user_id = %s AND disease_id = %s', (user_id, disease_id))
        result = fetch_data(cur)
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500