from flask import Flask, render_template, request
import mbta_helper
import urllib.parse

app = Flask(__name__)


@app.route("/", methods = ["GET","POST"])
def caclulate():
    if request.method == "POST":
        street = request.form["street"]
        city = request.form["city"]
        state = request.form["state"]
        zipcode = request.form["zipcode"]
        fulladdress = f"{street},{city},{state},{zipcode}"
        fulladdress = urllib.parse.quote_plus(fulladdress)
        app.logger.info(fulladdress)
        try: 
            if fulladdress: 
                closestStation = mbta_helper.find_stop_near(fulladdress)
                return render_template(
                    "result.html",
                    closestStation = closestStation,
                    street = street, 
                    city = city, 
                    state = state,
                    zipcode = zipcode,
                )
            else:
                return render_template("index.html", error = True)
        except:
            return render_template("index.html", error = None)

    return render_template("index.html", error = None)


if __name__ == "__main__":
    app.run(debug=True)