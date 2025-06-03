import os
import requests

from flask import jsonify, request
from . import users_bp
from ... utils.db_utils import *

@users_bp.route('/list', methods=['GET'])
def list_users():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.users')
        result = fetch_data(cur)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            cur.close()
            conn.close()

@users_bp.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    realname = request.json['realname']
    email = request.json['email']
    date = request.json['date_birth']
    
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.users (user_name, password, real_name, email, date_bitrh, roll) VALUES (%s, %s, %s, %s, %s, %d)', (username, password, realname, email, date, 2))
        
        conn.commit()
        
        return jsonify({'message': 'User created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            cur.close()
            conn.close()


@users_bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.users WHERE username = %s AND password = %s', (username, password))
        result = fetch_data(cur)
        
        if len(result) > 0:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Login failed'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            cur.close()
            conn.close()
    
@users_bp.route('/get_user/{id}', methods=['GET'])
def get_user(id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.users WHERE id = %s', (id,))
        result = fetch_data(cur)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            cur.close()
            conn.close()

@users_bp.route('/update_user/{id}', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    o_password = request.json['o_password']
    n_password = request.json['n_password']
    realname = request.json['realname']
    date = request.json['date_birth']
    email = request.json['email']
    try:
        data = request.json
        conn = create_connection()
        cur = conn.cursor()
        
        # Lấy thông tin hiện tại
        cur.execute('SELECT * FROM public.users WHERE id = %s', (id,))
        result = cur.fetchone()
        if len(result) == 0:
            return jsonify({'message': 'User not found'}), 404
        
        current_realname = realname or result[1]
        current_username = username or result[2]
        current_o_password = o_password or result[3]
        current_n_password = n_password or result[4]
        date = date or result[5]
        email = email or result[6]
        
        if current_o_password == current_n_password:
            return jsonify({'message': 'New password must be different from old password'}), 400
        else:
            cur.execute('''UPDATE public.users 
                        SET username = %s, password = %s, realname = %s, email = %s, date_birth = %s
                        WHERE id = %s''', (current_username, current_n_password, current_realname, email, date, id))
            conn.commit()
        
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            cur.close()
            conn.close()

@users_bp.route('/delete_user/{id}', methods=['DELETE'])
def delete_user(id):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('''DELETE FROM public.users 
                    WHERE id = %s''', (id,))
        
        conn.commit()
        
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            cur.close()
            conn.close()