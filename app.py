from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask Setup
#################################################
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    news = mongo.db.news.find_one()
    image = mongo.db.imageurl.find_one()
    weather = mongo.db.marsweather.find_one()
    info = mongo.db.mars_info.find_one()
    hemis = mongo.db.mars_hemispheres.find()

    return render_template("index.html", news=news, image=image, weather=weather, info=info, hemis=hemis)


@app.route("/scrape")
def scraper():
    scrape_mars.scrape()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
