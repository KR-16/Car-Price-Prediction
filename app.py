from logging import debug
from flask import Flask,render_template,request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open("random_forest_regression_model.pkl","rb"))


@app.route(rule="/",methods = ["GET"])
def home():
    return render_template("main.html")

standard_to = StandardScaler()

@app.route("/predict",methods = ["POST"])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == "POST":
        Year = int(request.form["Year"])
        Present_price = float(request.form["Present_price"])
        Kms_Driven = float(request.form["Kms_Driven"])
        Owner_type = int(request.form["Owner"])
        Fuel_Type_Petrol = request.form["Fuel_Type_Petrol"]
        if Fuel_Type_Petrol == "Petrol":
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type_Petrol == "Diesel":
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        Year = 2021-Year
        Seller_Type_Individual = request.form["Seller_Type_Individual"]
        if Seller_Type_Individual == "Individual":
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Manual = request.form["Transmission_Manual"]
        if Transmission_Manual == "Manual":
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
        
        # These features in the model
        prediction = model.predict([[Present_price,Kms_Driven,Owner_type,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        calculate_output = round(prediction[0],2)

        if calculate_output < 0:
            return render_template("main.html",prediction_texts = "You will not be able to Sale these car")
        else:
            return render_template("main.html",prediction_texts = "Car can be retailed at a price of {}".format(calculate_output))


if __name__ == "__main__":
    app.run(debug = True)
