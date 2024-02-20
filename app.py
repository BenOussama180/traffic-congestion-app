import pickle
from flask import Flask, render_template
from flask import request, jsonify
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import random
import pandas as pd


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/stepper")
def stepper():
    return render_template("stepper.html")


with open("./models/decision_tree_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        scaler = MinMaxScaler()
        encoder = LabelEncoder()

        inputs = dict(
            [
                ("midday", ""),
                ("Total", 0),
                ("TruckCount", 0),
                ("BusCount", 0),
                ("BikeCount", 0),
                ("CarCount", 0),
                ("Day of the week", 0),
                ("Date", 0),
                ("Time", "00:00"),
            ]
        )

        for i in range(len(data["Time"])):
            if data["Time"][i] == ":":
                if int(data["Time"][i - 1]) > 12:
                    inputs["midday"] = "PM"
                else:
                    inputs["midday"] = "AM"
                break

        match data["Total"]:
            case "-10":
                inputs["Total"] = random.randint(1, 10)
            case "10-20":
                inputs["Total"] = random.randint(10, 20)
            case "20-40":
                inputs["Total"] = random.randint(20, 40)
            case "40-80":
                inputs["Total"] = random.randint(40, 80)
            case "+100":
                inputs["Total"] = random.randint(100, 500)
            case _:
                inputs["Total"] = random.randint(1, 500)

        inputs["TruckCount"] = inputs["Total"] / 4
        inputs["BusCount"] = inputs["Total"] / 4
        inputs["BikeCount"] = inputs["Total"] / 4
        inputs["CarCount"] = inputs["Total"] / 4

        time_object = pd.to_datetime(data["Time"], format="%H:%M")

        inputs["Time"] = (
            time_object.hour * 3600 + time_object.minute * 60 + time_object.second
        )

        # get the day from the date my format is "2024-09-01"
        inputs["Date"] = int(data["Date"].split("-")[2])

        inputs["Day of the week"] = data["dayOfTheWeek"]

        # apply min max scaler to numerical columns
        inputs["Time"] = scaler.fit_transform([[inputs["Time"]]])
        inputs["Date"] = scaler.fit_transform([[inputs["Date"]]])
        inputs["TruckCount"] = scaler.fit_transform([[inputs["TruckCount"]]])
        inputs["BusCount"] = scaler.fit_transform([[inputs["BusCount"]]])
        inputs["BikeCount"] = scaler.fit_transform([[inputs["BikeCount"]]])
        inputs["CarCount"] = scaler.fit_transform([[inputs["CarCount"]]])
        inputs["Total"] = scaler.fit_transform([[inputs["Total"]]])
        # apply label encoder to categorical columns
        inputs["midday"] = encoder.fit_transform([[inputs["midday"]]])
        inputs["Day of the week"] = encoder.fit_transform([[inputs["Day of the week"]]])

        prediction = model.predict([inputs])

        result = {"prediction": prediction.tolist()}

        return jsonify(
            {
                "result": result,
                "message": "Prediction successful",
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
