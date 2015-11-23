import os
import json
import re
import shutil
from copy import deepcopy
from contextlib import closing
from jinja2 import Template, FileSystemLoader, Environment

TMPL_PATH = "templates/"
STATIC_PATH = "static/"
SLIDES_PATHS = [{'page': 'photos_%s' % name,
                 'folder': 'slides/%s/' % name}
                    for name in ['vaudevire', 'rjmuna', 'other']]
                

CAPTIONS_FILE = "_ATTRIBUTIONS.txt"
OUTPUT = "site/"

PAGES = ["index", "gallery", "video", "bio", "booking", "photos_rjmuna", "photos_vaudevire", "photos_other"]
NAV_PAGES = ["index", "gallery", "video", "bio", "booking"]

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
                            "id":t} for t in pages
                                    if t in NAV_PAGES]}
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
    all_slides = {}
    for slide_info in SLIDES_PATHS:
        print "copying %(page)s slides" % slide_info
        slides_paths = []
        try:
            os.makedirs(os.path.join(OUTPUT, STATIC_PATH, slide_info['folder']))
        except OSError, e:
            ## dir exists
            pass

        captions_path = os.path.join(slide_info['folder'], CAPTIONS_FILE)
        with closing(open(captions_path, "r")) as f:
            captions = json.loads(f.read())['captions']
        for s in [l for l in os.listdir(slide_info['folder']) if re.match("^.*\.(jpg|jpeg|png)$", l)]:
            output_path = os.path.join(STATIC_PATH, slide_info['folder'], s)
            shutil.copyfile(os.path.join(slide_info['folder'], s), os.path.join(OUTPUT, output_path))
            title = captions[s] if s in captions.keys() else s
            slides_paths.append({"title":title, "href":"/%s" % output_path})
        all_slides.update({slide_info['page']: slides_paths})
    return all_slides

if __name__ == "__main__":
    run_compilation()
