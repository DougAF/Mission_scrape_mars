# imports
from flask import Flask, current_app, jsonify, render_template
from flask_pymongo import PyMongo
import scrape_mars

#Flask instance
app = Flask(__name__)
#link to DB
mongo = PyMongo(app)

# # create index 
# @app.route("/")
# def index():
    
#     else:
#         return current_app.send_static_file('index.html')

# create scrape 
# @app.route("/scrape")
# def scrape():

# if __name__ == "__main__":
#     app.run(debug=True)