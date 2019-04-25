# imports
from flask import Flask, current_app, jsonify, render_template, redirect

from flask_pymongo import PyMongo

import pymongo

import scrape_mars

#Flask instance
app = Flask(__name__)
# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")
# Connect to a database. Will create one if not already available.
db = client.mars_data


# create index 
@app.route("/")
def index():
#         # Store the entire dict collection in a dict  dict(db.mars_data.find())
    mars = mongo.db.mars_data.find_one()
    return render_template('index.html', mars=mars)

# create scrape 
@app.route("/scrape")
def scrape():
    scrape_mars_dict = scrape_mars.scrape()
    mars_data = db.mars_data
    mars_data.update(
        {},
        scrape_mars_dict,
        upsert=True
    )
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)