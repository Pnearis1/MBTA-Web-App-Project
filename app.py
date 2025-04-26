from flask import Flask, render_template, request
from mbta_helper import find_stop_near
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place_name = request.form.get("place_name")
    try:
        station_name, wheelchair_accessible = find_stop_near(place_name)
        if wheelchair_accessible:
            accessibility = "This station is wheelchair accessible."
        else:
            accessibility = "This station is not wheelchair accessible."
        return render_template("result.html", place=place_name, station_name=station_name, accessibility=accessibility)
    except Exception as e:
        return render_template("error.html", error_message=str(e))


if __name__ == "__main__":
    app.run(debug=True)
