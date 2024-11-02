import pandas as pd
from flask import Flask, jsonify, request, render_template
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load and prepare the dataset
data = pd.read_csv('diabetes.csv')
X = data.drop('Outcome', axis=1)
y = data['Outcome']

# Scale the data and train the model
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = LogisticRegression()
model.fit(X_scaled, y)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = [
        float(data['Pregnancies']),
        float(data['Glucose']),
        float(data['BloodPressure']),
        float(data['SkinThickness']),
        float(data['Insulin']),
        float(data['BMI']),
        float(data['DiabetesPedigreeFunction']),
        float(data['Age'])
    ]
    
    # Scale input data and make prediction
    scaled_data = scaler.transform([input_data])
    prediction = model.predict(scaled_data)
    probability = model.predict_proba(scaled_data)[0][1] * 100  # Probability of diabetes

    # Return JSON response
    return jsonify({
        'prediction': int(prediction[0]),  # 1 for diabetic, 0 for not diabetic
        'probability': probability
    })

if __name__ == '__main__':
    app.run(debug=True)
