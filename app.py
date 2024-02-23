from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
import os
import numpy as np
#also need pip install openpyxl

app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/compare', methods=['POST'])
def compare():
    if request.method == 'POST':
        # Get the uploaded files
        original_file = request.files['excelFile1']
        review_file = request.files['excelFile2']

        # Save the uploaded files to temporary location
        UPLOAD_FOLDER = 'uploads'
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        original_path = os.path.join(UPLOAD_FOLDER, original_file.filename)
        review_path = os.path.join(UPLOAD_FOLDER, review_file.filename)
        original_file.save(original_path)
        review_file.save(review_path)

        # Read Excel files
        dforiginal = pd.read_excel(original_path)
        dfreview = pd.read_excel(review_path)

        # Compare values
        comparevalues = dforiginal.values == dfreview.values 
        print(comparevalues)

        # Find differences
        rows, cols = np.where(comparevalues == False)

        # Update differences
        for item in zip(rows, cols):
            value1 = str(dforiginal.iloc[item[0], item[1]])
            value2 = str(dfreview.iloc[item[0], item[1]])
            # Cast the columns to string before assigning string values
            dforiginal.iloc[item[0], item[1]] = 'Incorrect'.format(str(value1), str(value2))

        # Save to output CSV file
        output_file_path = os.path.join(UPLOAD_FOLDER, "output.csv")
        dforiginal.to_csv(output_file_path, index=False)

        # Remove temporary files
        os.remove(original_path)
        os.remove(review_path)

        return redirect(url_for('download', filename="output.csv"))

@app.route('/download/<filename>')
def download(filename):
    UPLOAD_FOLDER = 'uploads'  # Define UPLOAD_FOLDER here or globally
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)