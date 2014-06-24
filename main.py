from flask import Flask, render_template
import os
from contextlib import closing

app = Flask(__name__,
            static_folder="site/static")

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
@app.route("/<path:request_path>/")
def main(request_path=""):
    """
    Serve the files generically.
    """
    f_path = os.path.join(BASE_PATH, "site/", request_path, "index.html")
    print "looking for %s" % f_path
    if not os.path.exists(f_path):
        return "404"
    with closing(open(f_path, "r")) as f:
        return f.read()

if __name__ == "__main__":
    app.run("0.0.0.0", 8000)
