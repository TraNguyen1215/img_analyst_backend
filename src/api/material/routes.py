import os
import uuid
import time

from flask import jsonify, request, send_file
from . import material_bp
from ...utils.db_utils import *
from werkzeug.utils import secure_filename

@material_bp.route('/', methods=['GET'])# Lấy tất cả dữ liệu bản tin
def get_all_news():
    try:
        conn = create_connection()
        if conn is None:
            raise Exception("Could not establish a connection to the database.")
        
        cur = conn.cursor()
        
        # Lấy tất cả dữ liệu từ bảng material và cột vnnames từ bảng diseases
        cur.execute('''
            SELECT material.id, material.title, material."desc", material.create_at, material.dir, material.name,material.id_deas, diseases.vnname
            FROM public.material
            JOIN public.diseases ON material.id_deas = diseases.id
        ''')
            
        data = fetch_data(cur)
        
        return jsonify({'data': data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            conn.close()

@material_bp.route('/', methods=['POST'])
def post_news():
    original_title = request.form.get('original_title')
    description = request.form.get('description')
    create_at = time.strftime('%Y-%m-%d %H:%M:%S')
    id_deas = request.form.get('id_deas')
    id_deas = int(id_deas) if id_deas else 0
    
    # Kiểm tra file đính kèm
    if 'file' not in request.files:
        return jsonify({'error': 'No file part!'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file!'}), 400
    
    # Thiết lập thư mục lưu file
    upload_folder = './files/'
    os.makedirs(upload_folder, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

    # Tạo tên file mới với UUID
    rename_title = str(uuid.uuid4())  # Sử dụng uuid4 để tạo UUID ngẫu nhiên
    filename = secure_filename(file.filename)  # Đảm bảo tên file an toàn
    name = f"{rename_title}_{filename}"
    path_file = os.path.join(upload_folder, f"{rename_title}.pdf")  # Thay đổi cách tạo đường dẫn
    url = f"/{rename_title}.pdf/" or f"/{rename_title}.docx/"
    
    try:
        # Lưu file vào thư mục upload
        file.save(path_file)
        
        # Kết nối database
        conn = create_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed!'}), 500
        
        # Thực thi câu lệnh SQL
        with conn.cursor() as cur:
            cur.execute(''' 
                INSERT INTO public.material
                (title, "desc", create_at, dir, id_deas, name)
                VALUES (%s, %s, %s, %s, %s, %s);
            ''', (original_title, description,create_at, url,id_deas, rename_title))
            conn.commit()

        return jsonify({'message': 'Data has been successfully added!'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            conn.close()

@material_bp.route('/<news_path>/', methods=['GET'])
def get_news(news_path):
    try:
        conn = create_connection()
        if conn is None:
            raise Exception("Could not establish a connection to the database.")
        
        cur = conn.cursor()
        print(f"Received file: {news_path.strip('.pdf')}")
        title = news_path.strip('.pdf')
        
        # Nếu duong_dan là well_code và ten_tep chứa title thì trả về file
        cur.execute('''
            SELECT dir, name FROM 
                public.material
            WHERE
                dir = %s AND name LIKE %s ; 
        ''', (f'/{news_path}/', f'%{title}%'))
        
        result = cur.fetchone()
        print(result[1])

        # Lấy đường dẫn cơ sở mặc định nơi tệp chạy
        base_path = os.path.join(os.getcwd(), './files/')

        if result is None:
            return jsonify({'error': 'No file found for the given pathll; m.'}), 404

        # Tạo đường dẫn đầy đủ đến tệp
        path_file = os.path.join(base_path+result[1]+'.pdf')  # Thay đổi cách tạo đường dẫn
        print(path_file)

        # Kiểm tra tệp có tồn tại không
        if not os.path.exists(path_file):
            return jsonify({'error': 'File does not exist.'}), 404

        return send_file(path_file, as_attachment=True, mimetype='application/pdf')

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
            
# cập nhật bản tin
@material_bp.route('/<int:id>/', methods=['PUT'])
def update_news(id):
    title = request.json.get('title')
    description = request.json.get('description')
    id_deas = request.json.get('id_deas')
    id_deas = int(id_deas) if id_deas else 0
    update_at = time.strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        conn = create_connection()
        if conn is None:
            raise Exception("Could not establish a connection to the database.")
        
        cur = conn.cursor()
        
        cur.execute('''
            UPDATE public.material
            SET title = %s, "desc" = %s, id_deas = %s, update_at = %s
            WHERE id = %s;
        ''', (title, description, id_deas, id, update_at))
        
        conn.commit()
        
        return jsonify({'message': 'Data has been successfully updated!'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            conn.close()
            
            
# Xóa bản tin

@material_bp.route('/<int:id>/', methods=['DELETE'])
def delete_news(id):
    try:
        conn = create_connection()
        if conn is None:
            raise Exception("Could not establish a connection to the database.")
        
        cur = conn.cursor()
        
        cur.execute('''
            DELETE FROM public.material
            WHERE id = %s;
        ''', (id,))
        
        conn.commit()
        
        return jsonify({'message': 'Data has been successfully deleted!'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if conn:
            conn.close()
    
# đuong dẫn đến file
@material_bp.route('/img/<int:image_id>', methods=['GET'])
def get_image(image_id):
    try:
        # Kết nối đến cơ sở dữ liệu
        conn = create_connection()
        if conn is None:
            raise Exception("Could not establish a connection to the database.")
        
        cur = conn.cursor()
        
        # Truy vấn đường dẫn ảnh theo ID
        cur.execute('SELECT path FROM public.histories WHERE id = %s;', (image_id,))
        result = cur.fetchone()
        
        if not result:
            return jsonify({'error': 'Image not found'}), 404
        
        image_path = result[0]  # Đường dẫn ảnh
        
        # Kiểm tra file ảnh có tồn tại không
        if not os.path.exists(image_path):
            return jsonify({'error': 'Image file not found'}), 404
        
        # Trả về ảnh
        return send_file(image_path, mimetype='image/jpeg')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if conn:
            conn.close()
