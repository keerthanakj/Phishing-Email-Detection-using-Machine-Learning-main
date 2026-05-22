from flask import Flask, render_template, request, jsonify
import joblib
import os

app = Flask(__name__)

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'phishing_email_detector.joblib')
model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the email text from the form
        email_text = request.form.get('email_text')
        
        if not email_text:
            return jsonify({'error': 'No email text provided'}), 400
        
        # Make prediction
        prediction = model.predict([email_text])[0]
        probabilities = model.predict_proba([email_text])[0]
        
        # Prepare results
        result = {
            'is_phishing': bool(prediction),
            'confidence': {
                'legitimate': float(probabilities[0]),
                'phishing': float(probabilities[1])
            },
            'email_text': email_text
        }
        
        return render_template('result.html', result=result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 