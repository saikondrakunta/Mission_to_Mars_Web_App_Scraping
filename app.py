from flask import Flask,render_template,redirect
import scrape_mars
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_database"
mongo = PyMongo(app)

mongo.db.mars_collection.drop()
# main index route
@app.route("/")
def index():
    mars_collection=mongo.db.mars_collection.find_one()
    
    return render_template('index.html', mars_collection=mars_collection)

# the scrapper route
@app.route("/scrape")
def scraper():
    mars_collection=mongo.db.mars_collection
    mars_data=scrape_mars.scrape()
    mars_collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

#run the app
if __name__ == '__main__':
    app.run(debug=True)