from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load models and scaler
rf_model = joblib.load('RandomForestClassifier.pkl')
scaler = joblib.load('Standardscaler.pkl')

# Map predictions to readable labels
traffic_map = {
    1: "Low Traffic",
    2: "Medium Traffic",
    3: "High Traffic",
    4: "Very High",
    5: "Severe Jam"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        # Get input values
        coded_day = int(request.form['coded_day'])
        zone = int(request.form['zone'])
        weather = int(request.form['weather'])
        temp = float(request.form['temperature'])

        features = np.array([[coded_day, zone, weather, temp]])
        features_scaled = scaler.transform(features)
        pred = rf_model.predict(features_scaled)[0]

        prediction = traffic_map.get(pred, "Unknown")

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
