from flask import Flask, render_template, request
import os
import cv2
from PIL import Image
from keras.models import load_model
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

model = load_model("myModel.keras")

# Define the path to the uploads folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def preprocess_image(image):
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64, 64))
    image = np.array(image)
    image = image / 255.0
    return image
@app.route('/cancer')
def cancer():
    return render_template('cancer.html')

@app.route('/cancertypes')
def cancertypes():
    return render_template('cancertypes.html')

@app.route('/govt')
def govt():
    return render_template('govt.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        cancertype=request.form['cancertype']
        # Get the uploaded image
        uploaded_image = request.files['image']

        if uploaded_image:
            try:
                # Save the uploaded image to the "uploads" folder
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image.filename)
                uploaded_image.save(upload_path)

                # Read and preprocess the uploaded image
                image = cv2.imread(upload_path)
                image = preprocess_image(image)

                prediction = model.predict(np.expand_dims(image, axis=0))

                # Determine the result based on the prediction
                result = "Tumor Detected" if prediction > 0.5 else "No Tumor Detected"
                surety =  int(prediction[0][0] * 100)

                # Save the data in the "deepcancer" collection in Firebase
                db.collection('deepcancer').add({
                    'name': name,
                    'email': email,
                    'phone_number': phone_number,
                    'image_url': UPLOAD_FOLDER,  
                    'result': result,
                    'surety': surety,
                    'timestamp': firestore.SERVER_TIMESTAMP,
                    'cancertype':cancertype
                })

                if result == "Tumor Detected":
                    return render_template('result.html', result=result, surety="Surety: " + str(surety) + "%", prediction=prediction)
                else:
                    return render_template('result.html', result=result, prediction=prediction)

            except Exception as e:
                return f'Error processing image: {str(e)}'

    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
