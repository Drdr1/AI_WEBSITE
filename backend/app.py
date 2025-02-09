from flask import Flask, request, jsonify, send_from_directory
import os
import shutil

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Serve static files from the "public" folder
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../public', filename)

# Default route to serve the main page (login.html)
@app.route('/')
def index():
    return send_from_directory('../public', 'login.html')

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == 'password':
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# Contact form endpoint
@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    message = data.get('message')
    
    print(f"Contact form submission: {name}, {phone}, {email}, {message}")
    return jsonify({"message": "Thank you for contacting us!"})

# Service request endpoint
@app.route('/service/<int:service_id>', methods=['POST'])
def handle_service(service_id):
    services = {
        1: "التعرف عن المجرمين",
        2: "الكشف عن المجرمين",
        3: "تزوير العملات"
    }
    
    if service_id in services:
        return jsonify({"message": f"تم طلب خدمة: {services[service_id]}"})
    else:
        return jsonify({"error": "الخدمة غير موجودة"}), 404

# Serve uploaded files
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# File upload endpoint
@app.route('/upload/<int:service_id>', methods=['POST'])
def upload_file(service_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    print(f"Uploaded file saved to: {file_path}")

    # Process the image based on the service ID
    if service_id == 1:
        result = enhance_photo(file_path)
    elif service_id == 2:
        result = detect_criminals(file_path)
    elif service_id == 3:
        result = detect_counterfeit(file_path)
    else:
        return jsonify({"error": "Invalid service ID"}), 400

    print(f"Processed image saved to: {result['output_filename']}")
    return jsonify({
        "message": "تم معالجة الصورة بنجاح",
        "image_url": f"/uploads/{result['output_filename']}"
    })

# AI model functions (simulated)
def enhance_photo(file_path):
    output_filename = "enhanced_" + os.path.basename(file_path)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    shutil.copy(file_path, output_path)
    return {"output_filename": output_filename}

def detect_criminals(file_path):
    output_filename = "detected_" + os.path.basename(file_path)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    shutil.copy(file_path, output_path)
    return {"output_filename": output_filename}

def detect_counterfeit(file_path):
    output_filename = "counterfeit_" + os.path.basename(file_path)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    shutil.copy(file_path, output_path)
    return {"output_filename": output_filename}

if __name__ == '__main__':
    app.run(debug=True)
