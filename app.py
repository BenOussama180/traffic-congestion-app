# import pickle
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/stepper")
def stepper():
	return render_template("stepper.html")

if __name__ == '__main__':
	app.run(debug=True)


# with open('model.pkl', 'rb') as model_file:
# model = pickle.load(model_file)

# @app.route('/predict', methods=['POST'])
# def predict():
# try:
# # Get the input data from the request
# data = request.get_json()

# # Convert the received data into a format suitable for prediction
# # Assuming the input data is in a list format
# input_data = [float(val) for val in data['inputs']]

# # Make prediction using the loaded model
# prediction = model.predict([input_data])

# # Prepare the response
# result = {'prediction': prediction.tolist()}

# return jsonify(result)

# except Exception as e:
# return jsonify({'error': str(e)})
