from flask import Flask, make_response, render_template, request, send_file 
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

        # Read Excel files
        dforiginal = pd.read_excel(original_file)
        dfreview = pd.read_excel(review_file)

        # Compare values
        comparevalues = dforiginal.values == dfreview.values 

        # Find differences
        rows, cols = np.where(comparevalues == False)

        # Update differences
        for item in zip(rows, cols):
            value1 = str(dforiginal.iloc[item[0], item[1]])
            value2 = str(dfreview.iloc[item[0], item[1]])
            # Cast the columns to string before assigning string values
            dforiginal.iloc[item[0], item[1]] = 'Incorrect'.format(str(value1), str(value2))

        # Save to output CSV file in memory
        output_csv = dforiginal.to_csv(index=False)

        # Create a response object
        response = make_response(output_csv)
        
        # Set headers to force file download
        response.headers['Content-Disposition'] = 'attachment; filename=output.csv'
        response.headers['Content-Type'] = 'text/csv'

        return response

if __name__ == '__main__':
    app.run(debug=True)