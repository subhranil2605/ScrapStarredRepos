from flask import Flask, render_template, request
from scraping_multiple_pages import *

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user = request.form["nm"]
        option = request.form["gridRadios"]
        url = f"https://github.com/{user}?tab=stars"
        
        stars = []
        while True:
            soup = getdata(url)
            stars.append(scrape_stars(soup))
            url = get_next_page(soup)
            if not url:
                break

        return render_template("index.html", stars=stars, username=user)
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run()
