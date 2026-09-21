import os
import json

from flask import Flask, request, render_template,redirect,url_for,jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

#Task 1: JSON API Route
@app.route('/api', methods=['GET'])
def get_api_data():
    try:
        with open('data.json','r') as f:
            data = json.load(f)
        return jsonify(data),200
    except Exception as e:
        return jsonify({error: str(e)}),500

#Task 2: Home / Form Page
@app.route('/')
def home():
    return render_template('index.html')

#Task 2: Form Submission Handling
@app.route('/submit',methods=['POST'])
def submit():
    form_data=dict(request.form)
    try:
        #Connect and insert in mongodb atlas
        MONGODB_URI = os.getenv('MONGODB_URI')

        # Create a new client and connect to the server
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        db = client['flaskAssignmentDb']
        collection = db['flask-assignment']

        #insert data
        collection.insert_one(form_data)
        client.close()

        #On success: redirect to success page
        return redirect(url_for('success_page'))
    except Exception as e:
        #On error: render form page again displaying error message
        return render_template('index.html',error=f"DataBase Error: {str(e)}")

@app.route('/success')
def success_page():
    return render_template('success.html')

@app.route('/submittodoitem',methods=['POST'])
def submittodoitem():
    form_data=dict(request.form)
    try:
        #Connect and insert in mongodb atlas
        MONGODB_URI = os.getenv('MONGODB_URI')

        # Create a new client and connect to the server
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        db = client['GitAssignmentDb']
        collection = db['Git-assignment']

        #insert data
        collection.insert_one(form_data)
        client.close()

        #On success: redirect to success page
        return redirect(url_for('success_page'))
    except Exception as e:
        #On error: render form page again displaying error message
        return render_template('index.html',error=f"DataBase Error: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)