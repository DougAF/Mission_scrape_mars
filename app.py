# imports
from flask import Flask, current_app, jsonify, render_template, redirect

from flask_pymongo import PyMongo

import scrape_mars

#Flask instance
app = Flask(__name__)
# Create connection variable
mongo = PyMongo(app, uri="mongodb://localhost:27017")

# create index 
@app.route("/")
def index():
#         # Store the entire dict collection in a dict  dict(db.mars_data.find())
    mars_app_dict = mongo.db.collection.find_one()
    print("scrape_mars_dict")
    return render_template('index.html', mars_data_dict= mars_app_dict)
# #         return current_app.send_static_file('index.html')

# create scrape 
@app.route("/scrape")
def scrape():
    scrape_mars_dict = scrape_mars.scrape()
    mars_data = mongo.db.mars
    mars_data.update(
        {},
        scrape_mars_dict,
        upsert=True
    )
    return redirect("http://localhost:5000/")

if __name__ == "__main__":
    app.run(debug=True)