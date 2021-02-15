# Import dependencies
from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsDB")


# Create route that renders index.html template
@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()

    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape_data():
    # Run scraped fuctions
    scraped_data = scrape_mars.scrape()
    mongo.db.collection.update({}, scraped_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5006)