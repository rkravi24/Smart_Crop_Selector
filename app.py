from flask import Flask,request,render_template
import numpy as np
import pandas
import sklearn
import pickle
import requests

app = Flask(__name__)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
model = pickle.load(open('model.pkl','rb'))
sc = pickle.load(open('standscaler.pkl','rb'))
ms = pickle.load(open('minmaxscaler.pkl','rb'))
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#++++++++++++++++++++ JSONBin.io details ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
JSONBIN_BIN_ID = "67addfb8acd3cb34a8e06bd8"
JSONBIN_API_KEY = "$2a$10$FSoZINyJcgRUh6lUY2xpuOH5WgwdMAPKnNYVs5OJymxsKlDmWXgRq"
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest"

FIND_SEEDS_URL = "https://api.jsonbin.io/v3/b/67ade000acd3cb34a8e06c1a"
HEADERS = {
    "X-Master-Key": "$2a$10$FSoZINyJcgRUh6lUY2xpuOH5WgwdMAPKnNYVs5OJymxsKlDmWXgRq"
}
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/')
def home():
    return render_template("home.html")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++++++++++++++++++++++++++++++++PREDICT CROP++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++++++++++++++++++++++++++++++++FIND SEEDS TEMPLATE+++++++++++++++++++++++++++++++++++++++++
@app.route('/findseeds', methods=['GET', 'POST'])
def findseeds():
    crop = None
    bestSeeds = None
    error = None
    if request.method == 'POST':
        crop_name = request.form.get('cropName').lower()
        # Fetch JSON data from JSONBin.io
        try:
            response = requests.get(FIND_SEEDS_URL, headers=HEADERS)
            if response.status_code == 200:
                data = response.json().get("record", {})
                seeds = data.get("seeds", [])
                # Find matching crop
                for item in seeds:
                    if item["crop"].lower() == crop_name:
                        crop = crop_name.capitalize()
                        bestSeeds = item["bestSeeds"]
                        break
                if not bestSeeds:
                    error = f"No seeds found for {crop_name}."
            else:
                error = "Error fetching data. Try again later."
        except Exception as e:
            error = f"No internet connection"

    return render_template('find-seeds.html', crop=crop, bestSeeds=bestSeeds, error=error)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++++++++++++++++++++++++++ HOW TO SOW TEMPLATE ++++++++++++++++++++++++++++++++++++++++++++++++++++
def fetch_crop_data():
    try:
        response = requests.get(JSONBIN_URL, headers=HEADERS)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("record", {}).get("crops", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from JSONBin: {e}")
        return []
    
@app.route('/howtosow', methods=['GET', 'POST'])
def takecare():
    if request.method == 'POST':
        crop_name = request.form.get('cropname').lower() 
        crops = fetch_crop_data()
        crop_details = None

        for crop in crops:
            if crop["name"].lower() == crop_name:
                crop_details = crop
                break
        if crop_details:
            return render_template('take-care.html', 
                                   crop=crop_details["name"].capitalize(),
                                   seed_type=crop_details["seed_type"],
                                   land_required_per_kg=crop_details["land_required_per_kg"],
                                   manure=crop_details["manure"],
                                   fertilizers=crop_details["fertilizers"],
                                   sowing_practices=crop_details["sowing_practices"])
        
        else:
            return render_template('take-care.html', error=f"Crop '{crop_name}' not found")
    return render_template('take-care.html')
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route('/predictpage')
def predictpage():
    return render_template('predict_page.html')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route("/predict",methods=['POST'])
def predict():
    N = request.form['Nitrogen']
    P = request.form['Phosporus']
    K = request.form['Potassium']
    temp = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['Ph']
    rainfall = request.form['Rainfall']

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    scaled_features = ms.transform(single_pred)
    final_features = sc.transform(scaled_features)
    prediction = model.predict(final_features)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        result = "{} is the best crop to be cultivated right there".format(crop)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    return render_template('predict_page.html',result = result)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# python main
if __name__ == "__main__":
    app.run(debug=True)