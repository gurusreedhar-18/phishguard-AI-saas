from flask import Flask, render_template, request
import joblib
from feature_extraction import extract_features

app = Flask(__name__)

# Load trained AI model
model = joblib.load("model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    url = None

    if request.method == "POST":
        url = request.form["url"]
        features = extract_features(url)
        prediction = model.predict([features])[0]

        if prediction == 1:
            result = "Phishing URL"
        else:
            result = "Legitimate URL"

    return render_template("index.html", result=result, url=url)

if __name__ == "__main__":
    app.run(debug=True)

