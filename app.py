from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
try:
    with open('heart_disease_model.pkl', 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/predict', methods=['POST'])
def predict_page():
    if model is None:
        return jsonify({'error': 'Model not loaded properly. Please check the server logs.'}), 500

    try:
        if not request.is_json:
            return jsonify({'error': 'Request content type must be application/json'}), 400

        data = request.get_json()

        required_features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                              'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

        input_features = []
        for feature in required_features:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
            try:
                input_features.append(float(data[feature]) if feature not in ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'] else int(data[feature]))
            except ValueError:
                return jsonify({'error': f'Invalid value for feature: {feature}'}), 400

        input_features = np.array([input_features])

        prediction = model.predict(input_features)

        return jsonify({'prediction': int(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
