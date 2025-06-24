from flask import Flask, jsonify, render_template, request, redirect, url_for, send_file
import os
import subprocess
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  # Directory to save uploaded files
OUTPUT_FOLDER = 'output'   # Directory to save encrypted files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure the upload and output folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encryption')
def encryption():
    return render_template('encryption.html')  # Render the HTML form for file upload

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'encryptionKey' not in request.form:
        return jsonify({"message": "File or key not provided"}), 400

    file = request.files['file']
    encryption_key = request.form['encryptionKey']

    if file and encryption_key:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)  # Save uploaded file

        # Generate the output file names
        encrypted_file = os.path.join(app.config['OUTPUT_FOLDER'], 'encrypted_' + file.filename)
        perm_file = encrypted_file + '.perm'  # .perm file based on the encrypted file name

        # Run the encryption Python script with the uploaded file and key
        try:
            command = ['python3', './python/file_encryptor.py', file_path, encryption_key, encrypted_file]
            process = subprocess.run(command, capture_output=True, text=True)

            if process.returncode == 0:
                # Create a zip file containing the encrypted file and .perm file
                zip_filename = os.path.join(app.config['OUTPUT_FOLDER'], 'encrypted_package.zip')
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    zipf.write(encrypted_file, os.path.basename(encrypted_file))
                    if os.path.exists(perm_file):  # Ensure the .perm file exists
                        zipf.write(perm_file, os.path.basename(perm_file))
                    else:
                        print(f"Warning: Permission file does not exist: {perm_file}")

                # Redirect to the download page with the zip file link
                return redirect(url_for('download', filename='encrypted_package.zip'))
            else:
                return jsonify({"message": f"Encryption failed: {process.stderr}"}), 500
        except Exception as e:
            return jsonify({"message": f"Error occurred: {str(e)}"}), 500

@app.route('/decrypt_file', methods=['POST'])
def decrypt_file():
    # Ensure that both decryption key and files are provided
    if 'decryptionKey' not in request.form or len(request.files.getlist('input-files')) != 2:
        return jsonify({"message": "Please provide a decryption key and upload both the encrypted file and permission file"}), 400

    decryption_key = request.form['decryptionKey']
    files = request.files.getlist('input-files')  # Get the uploaded files (encrypted and .perm file)

    # Loop through the files to identify encrypted file and .perm file
    for file in files:
        if file.filename.endswith('.perm'):
            perm_file = file
        else:
            encrypted_file = file

    # Ensure both encrypted file and .perm file were provided
    if not encrypted_file or not perm_file:
        return jsonify({"message": "Both encrypted file and permission file are required"}), 400

    # Save the files to the upload folder
    encrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_file.filename)
    perm_file_path = os.path.join(app.config['UPLOAD_FOLDER'], perm_file.filename)

    encrypted_file.save(encrypted_file_path)
    perm_file.save(perm_file_path)

    # Generate the output file name for the decrypted file
    decrypted_file = os.path.join(app.config['OUTPUT_FOLDER'], 'decrypted_' + encrypted_file.filename)

    # Run the decryption Python script with the encrypted file, key, and permission file
    try:
        command = ['python3', './python/file_decryptor.py', encrypted_file_path, decryption_key, perm_file_path, decrypted_file]
        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode == 0:
            # Create a zip file containing the decrypted file
            zip_filename = os.path.join(app.config['OUTPUT_FOLDER'], 'decrypted_package.zip')
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                if os.path.exists(decrypted_file):  # Ensure the decrypted file exists
                    zipf.write(decrypted_file, os.path.basename(decrypted_file))
                else:
                    return jsonify({"message": "Decrypted file not found"}), 500

            # Redirect to the download page with the zip file link
            return redirect(url_for('download', filename='decrypted_package.zip'))
        else:
            return jsonify({"message": f"Decryption failed: {process.stderr}"}), 500
    except Exception as e:
        return jsonify({"message": f"Error occurred: {str(e)}"}), 500

@app.route('/download/<filename>')
def download(filename):
    # Render the download page with the file to download
    return render_template('download.html', filename=filename)

@app.route('/download_file/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"message": "File not found"}), 404

@app.route('/decrypt')
def decrypt():
    return render_template('decrypt.html')  # Render the HTML form for decryption

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
