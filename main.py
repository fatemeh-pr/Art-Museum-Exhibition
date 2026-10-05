import math
import requests
from flask import Flask, render_template, abort
from api import get_artworks, get_random_art, get_art_info
from api import GALLERIES

app = Flask(__name__)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404 


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/gallery/<string:gallery_name>/<int(min=1):page>")
def gallery(gallery_name, page):
    if gallery_name not in GALLERIES:
        abort(404)
    ARTS_PER_PAGE = 9
    offset = (page - 1) * ARTS_PER_PAGE
    gallery_title, artworks, counts = get_artworks(gallery_name=gallery_name,
                                                    number=ARTS_PER_PAGE,
                                                    offset=offset)
    total_pages = int(math.ceil(counts / ARTS_PER_PAGE))
    if page > total_pages:
        abort(404)
    return render_template("gallery.html", gallery_name=gallery_name, artworks=artworks, gallery_title=gallery_title, total_pages=total_pages, page=page)

    
@app.route("/artwork/<int:artwork_id>")
def artwork(artwork_id):
    try:
        artwork = get_art_info(artwork_id)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            abort(404)
        raise
    return render_template("artwork.html", artwork=artwork)


@app.route("/random_art")
def random_art():
    random_artwork = get_random_art()
    return render_template("random_art.html", artwork=random_artwork)


if __name__ == "__main__":
    app.run()
