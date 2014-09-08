import os
import re
import shutil
from copy import deepcopy
from contextlib import closing
from jinja2 import Template, FileSystemLoader, Environment

TMPL_PATH = "templates/"
STATIC_PATH = "static/"
SLIDES_PATH = "slides/"
OUTPUT = "site/"

PAGES = ["index", "photos", "video", "bio", "booking"]

def setup():
    shutil.rmtree(os.path.join(OUTPUT, STATIC_PATH))
    shutil.copytree(STATIC_PATH, os.path.join(OUTPUT, STATIC_PATH))

def tmpl_compile(tmpl_base, env_vars):
    out_path = str(OUTPUT)
    if tmpl_base != "index":
        out_path = os.path.join(out_path, tmpl_base)

    ## setup the environment for this template
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__name__)), "templates/")))
    tmpl_globals = deepcopy(env_vars)
    tmpl_globals.update({"current_page":tmpl_base})
    tmpl_globals.update({"slides":slides()})

    ## render and write
    template = env.get_template("%s.html" % tmpl_base, globals=tmpl_globals)
    try:
        os.makedirs(out_path)
    except OSError:
        pass ## directory exists, ignore
    with closing(open(os.path.join(out_path, "index.html"), "w")) as f_out:
        print "writing to %s" % out_path
        f_out.write(template.render())

def get_valid_templates():
    """
    Get all templates we will be working with (necessary for directory tree)
    """
    #return [f.rsplit(".")[0] for f in os.listdir(TMPL_PATH) if not re.match("^_.*$", f) and re.match(".*html$", f)]
    return [p for p in PAGES if os.path.exists(os.path.join(TMPL_PATH, "%s.html" % p))]

def compile_templates():
    pages = get_valid_templates()
    env_vars = {"nav_pages":[{"url":"/%s/" % t if t != "index" else "/",
                            "name":t.title() if t != "index" else "Home",
                            "id":t} for t in pages]}
    for tmpl in pages:
        print "working on %s" % tmpl
        tmpl_compile(tmpl, env_vars)

def run_compilation():
    setup()
    compile_templates()

def slides():
    """
    Assemble the slides.
    """
    print "copying slides"
    slides_paths = []
    try:
        os.mkdir(os.path.join(OUTPUT, STATIC_PATH, SLIDES_PATH))
    except OSError:
        ## dir exists, pass
        pass
    for s in [l for l in os.listdir(SLIDES_PATH) if re.match("^.*\.(jpg|jpeg)$", l)]:
        output_path = os.path.join(STATIC_PATH, SLIDES_PATH, s)
        shutil.copyfile(os.path.join(SLIDES_PATH, s), os.path.join(OUTPUT, output_path))
        slides_paths.append("/%s" % output_path)
    return slides_paths

if __name__ == "__main__":
    run_compilation()
