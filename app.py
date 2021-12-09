from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pandas
import os
import geopy
from geopy.geocoders import ArcGIS

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods = ['POST'])
def success():
    global file
    if request.method == 'POST':
        file = request.files['file']
        #file.save(secure_filename("uploaded" + file.filename))
        #with open("uploaded" + file.filename, "a") as f:
        #    f.write("this was added later")
        try:
            data = pandas.read_csv(file)
            data.columns = data.columns.str.lower()
            nom = ArcGIS()
            data["coordinates"] = data["address"].apply(nom.geocode)
            data['latitude'] = data['coordinates'].apply(lambda x: x.latitude if x != None else None)
            data['longitude'] = data['coordinates'].apply(lambda x: x.longitude if x != None else None)
            data = data.drop('coordinates',1)
            data.to_csv("edited_table.csv")
            return render_template("index.html", btn = "download.html", text = data.to_html())
        except:
            return render_template("index.html", text= 'Hmm it seems address wasnt found in this file, check the file and try again')

@app.route('/download')
def download():
    return send_file("edited_table.csv", attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run()
