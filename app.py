from flask import Flask, render_template, url_for, flash, redirect
import joblib
from flask import request
import numpy as np

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==7):
        loaded_model = joblib.load('hdp_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/predict', methods = ["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        
        if(len(to_predict_list)==7):
            result = ValuePredictor(to_predict_list,7)
    
    if(int(result)==1):
        prediction = "You have heart condition, Consult the doctor immediately"
    else:
        prediction = "You are safe. You have no dangerous symptoms !!! :-)"
    return(render_template("prediction_result.html", prediction_text=prediction))       

if __name__ == "__main__":
    # Use below for local flask deployment
    #app.run(debug=True)
    
    #Use below for AWS EC2 deployment
    app.run(host='0.0.0.0',port=8080)
